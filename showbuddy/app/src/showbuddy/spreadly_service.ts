/**
 * SpreadlyService Module
 * 
 * This module provides an interface to the spreadly.io API for extracting
 * information from business card images. It supports uploading images,
 * processing them, and retrieving the extracted data with session tracking.
 */

// Types for the business card data
export interface BusinessCardData {
  name?: string;
  title?: string;
  company?: string;
  email?: string;
  phone?: string;
  mobile?: string;
  website?: string;
  address?: string;
  city?: string;
  state?: string;
  zip?: string;
  country?: string;
  social?: {
    linkedin?: string;
    twitter?: string;
    facebook?: string;
    instagram?: string;
    [key: string]: string | undefined;
  };
  notes?: string;
  raw_text?: string;
  [key: string]: any;
}

export interface BusinessCardScanResult {
  sessionId: string;
  timestamp: string;
  scanId: string;
  cardData: BusinessCardData;
  imageUrl: string;
  confidence: number;
}

// Configuration interface
export interface SpreadlyConfig {
  apiKey: string;
  apiEndpoint?: string;
  timeout?: number;
  retryAttempts?: number;
}

/**
 * SpreadlyService class for interacting with spreadly.io
 */
export class SpreadlyService {
  private apiKey: string;
  private apiEndpoint: string;
  private timeout: number;
  private retryAttempts: number;

  /**
   * Creates a new SpreadlyService instance
   * @param config Configuration options for the scanner
   */
  constructor(config: SpreadlyConfig) {
    this.apiKey = config.apiKey;
    this.apiEndpoint = config.apiEndpoint || 'https://api.spreadly.io/v1/cards/parse';
    this.timeout = config.timeout || 30000; // 30 seconds default
    this.retryAttempts = config.retryAttempts || 3;
  }

  /**
   * Process a business card image and extract information
   * @param imageUri URI or path to the image file
   * @param sessionId Unique identifier for the recording session
   * @returns A promise resolving to the business card scan result
   */
  public async processImage(imageUri: string, sessionId: string): Promise<BusinessCardScanResult> {
    try {
      // Upload the image
      const uploadResult = await this.uploadImage(imageUri);
      
      // Process the image with OCR
      const scanResult = await this.extractCardData(uploadResult.imageId);
      
      // Format and return the result
      return this.formatResult(scanResult, imageUri, sessionId);
    } catch (error) {
      console.error('Error processing business card image:', error);
      throw new Error(`Failed to process business card: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * Process multiple business card images in batch
   * @param imageUris Array of image URIs or paths
   * @param sessionId Unique identifier for the recording session
   * @returns A promise resolving to an array of business card scan results
   */
  public async processMultipleImages(imageUris: string[], sessionId: string): Promise<BusinessCardScanResult[]> {
    const scanPromises = imageUris.map(uri => this.processImage(uri, sessionId));
    return Promise.all(scanPromises);
  }

  /**
   * Upload an image to the spreadably.io service
   * @param imageUri URI or path to the image file
   * @returns Promise resolving to the upload result
   */
  private async uploadImage(imageUri: string): Promise<{ imageId: string; uploadUrl: string }> {
    let attempts = 0;
    
    while (attempts < this.retryAttempts) {
      try {
        // Prepare the file for upload
        const formData = new FormData();
        
        // Handle different types of image URIs (file, http, base64, etc.)
        if (imageUri.startsWith('data:image')) {
          // Handle base64 image
          const blob = this.dataURItoBlob(imageUri);
          formData.append('file', blob, 'business_card.jpg');
        } else if (imageUri.startsWith('http')) {
          // Handle remote URL
          const response = await fetch(imageUri);
          const blob = await response.blob();
          formData.append('file', blob, 'business_card.jpg');
        } else {
          // Assume it's a file path or direct access
          formData.append('file', imageUri);
        }

        // Send the upload request
        const response = await fetch(`${this.apiEndpoint}/uploads`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.apiKey}`
          },
          body: formData,
          timeout: this.timeout
        });

        if (!response.ok) {
          throw new Error(`Upload failed with status: ${response.status}`);
        }

        const data = await response.json();
        return {
          imageId: data.id,
          uploadUrl: data.url
        };
      } catch (error) {
        attempts++;
        if (attempts >= this.retryAttempts) {
          throw error;
        }
        // Wait before retrying (exponential backoff)
        await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, attempts)));
      }
    }

    throw new Error('Upload failed after multiple attempts');
  }

  /**
   * Extract business card data from an uploaded image
   * @param imageId ID of the uploaded image
   * @returns Promise resolving to the extracted data
   */
  private async extractCardData(imageId: string): Promise<any> {
    let attempts = 0;
    
    while (attempts < this.retryAttempts) {
      try {
        const response = await fetch(`${this.apiEndpoint}/business-cards/scan`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            imageId: imageId,
            options: {
              enhancedOcr: true,
              confidenceScores: true
            }
          }),
          timeout: this.timeout
        });

        if (!response.ok) {
          throw new Error(`Extraction failed with status: ${response.status}`);
        }

        const data = await response.json();
        
        // Poll for completion if processing asynchronously
        if (data.status === 'processing') {
          return await this.pollForCompletion(data.jobId);
        }
        
        return data;
      } catch (error) {
        attempts++;
        if (attempts >= this.retryAttempts) {
          throw error;
        }
        // Wait before retrying
        await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, attempts)));
      }
    }

    throw new Error('Extraction failed after multiple attempts');
  }

  /**
   * Poll for the completion of an asynchronous scanning job
   * @param jobId ID of the scanning job
   * @returns Promise resolving to the scan result
   */
  private async pollForCompletion(jobId: string): Promise<any> {
    const maxAttempts = 30; // Maximum number of polling attempts
    let attempts = 0;
    
    while (attempts < maxAttempts) {
      try {
        const response = await fetch(`${this.apiEndpoint}/business-cards/jobs/${jobId}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${this.apiKey}`
          },
          timeout: this.timeout
        });

        if (!response.ok) {
          throw new Error(`Polling failed with status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.status === 'completed') {
          return data.result;
        } else if (data.status === 'failed') {
          throw new Error('Scanning job failed: ' + (data.error || 'Unknown error'));
        }
        
        // Wait before polling again
        await new Promise(resolve => setTimeout(resolve, 2000));
        attempts++;
      } catch (error) {
        throw error;
      }
    }

    throw new Error('Timed out waiting for job completion');
  }

  /**
   * Format the scan result into the standardized BusinessCardScanResult format
   * @param scanResult Raw scan result from the API
   * @param imageUri Original image URI
   * @param sessionId Session ID
   * @returns Formatted BusinessCardScanResult
   */
  private formatResult(scanResult: any, imageUri: string, sessionId: string): BusinessCardScanResult {
    return {
      sessionId: sessionId,
      timestamp: new Date().toISOString(),
      scanId: scanResult.id || `scan-${Date.now()}`,
      cardData: {
        name: scanResult.name,
        title: scanResult.title,
        company: scanResult.company,
        email: scanResult.email,
        phone: scanResult.phone,
        mobile: scanResult.mobile,
        website: scanResult.website,
        address: scanResult.address,
        city: scanResult.city,
        state: scanResult.state,
        zip: scanResult.zip,
        country: scanResult.country,
        social: scanResult.social || {},
        notes: scanResult.notes,
        raw_text: scanResult.raw_text
      },
      imageUrl: imageUri,
      confidence: scanResult.confidence || 0
    };
  }

  /**
   * Convert a data URI to a Blob object
   * @param dataURI The data URI string
   * @returns Blob object
   */
  private dataURItoBlob(dataURI: string): Blob {
    const byteString = atob(dataURI.split(',')[1]);
    const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
    
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    
    for (let i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
    }
    
    return new Blob([ab], { type: mimeString });
  }
}

/**
 * Factory function to create a SpreadlyService instance
 * @param config Configuration for the scanner
 * @returns A new SpreadlyService instance
 */
export function createSpreadlyService(config: SpreadlyConfig): SpreadlyService {
  return new SpreadlyService(config);
}

export default {
  createSpreadlyService,
  SpreadlyService
};