// simple-test.ts
import { createSpreadlyService, BusinessCardScanResult } from './spreadly_service';

/**
 * Simple test script for the Business Card Scanner module
 * 
 * This script mocks the fetch API to avoid actual network calls
 * and demonstrates how to use the scanner module.
 */

// Mock the global fetch function to avoid actual API calls
// @ts-ignore - Ignoring type issues with global fetch mocking
global.fetch = async (url: string, options?: any): Promise<any> => {
    console.log(`[MOCK] Fetch called: ${url}`);
    console.log(`[MOCK] Request headers:`, options?.headers || {});
    console.log(`[MOCK] Request method:`, options?.method || 'GET');

    // Mock response based on the endpoint called
    if (url.includes('/uploads')) {
        console.log('[MOCK] Handling image upload request');
        return {
            ok: true,
            json: async () => ({
                id: 'mock-image-id-123',
                url: 'https://api.spreadly.io/mock-image-url'
            })
        };
    }

    if (url.includes('/business-cards/scan')) {
        console.log('[MOCK] Handling card scanning request');
        return {
            ok: true,
            json: async () => ({
                id: 'mock-scan-result-456',
                name: 'Jane Smith',
                title: 'Chief Marketing Officer',
                company: 'Acme Corp',
                email: 'jane.smith@acmecorp.com',
                phone: '+1 (555) 123-4567',
                mobile: '+1 (555) 987-6543',
                website: 'www.acmecorp.com',
                address: '123 Business Avenue',
                city: 'San Francisco',
                state: 'CA',
                zip: '94105',
                country: 'USA',
                social: {
                    linkedin: 'linkedin.com/in/janesmith',
                    twitter: '@janesmith'
                },
                confidence: 0.95
            })
        };
    }

    // Default response for unhandled endpoints
    return {
        ok: false,
        status: 404,
        json: async () => ({ error: 'Not Found' })
    };
};

// Mock FormData for Node.js environment if needed
if (typeof FormData === 'undefined') {
    // @ts-ignore
    global.FormData = class FormData {
        append(key: string, value: any, filename?: string) {
            console.log(`[MOCK] FormData append: ${key}, ${filename || 'unnamed'}`);
        }
    };
}

/**
 * Run the test
 */
async function runTest() {
    console.log('-'.repeat(50));
    console.log('TESTING BUSINESS CARD SCANNER MODULE');
    console.log('-'.repeat(50));

    try {
        // Create the scanner with mock API key
        const scanner = createSpreadlyService({
            apiKey: process.env.SPREADLY_API_KEY,
            apiEndpoint: 'https://api.spreadly.io/v1'
        });

        console.log('✅ Scanner instance created successfully');

        // Test processing a single image
        console.log('\nTesting single image processing...');
        const singleResult = await scanner.processImage(
            'business_card_0.jpg',
            'test-session-001'
        );

        console.log('✅ Single image processed successfully');
        console.log('\nScan Result:');
        console.log(JSON.stringify(singleResult, null, 2));

        // Test processing multiple images
        console.log('\nTesting multiple image processing...');
        const imageUris = [
            'business_card_0.jpg',
            'business_card_0.jpg'
        ];

        const multiResults = await scanner.processMultipleImages(
            imageUris,
            'test-session-002'
        );

        console.log('✅ Multiple images processed successfully');
        console.log(`✅ Processed ${multiResults.length} business cards`);

        console.log('\nFirst result from batch:');
        console.log(JSON.stringify(multiResults[0], null, 2));

        console.log('-'.repeat(50));
        console.log('ALL TESTS PASSED SUCCESSFULLY! ✨');
        console.log('-'.repeat(50));

    } catch (error) {
        console.error('❌ TEST FAILED:');
        console.error(error);
        process.exit(1);
    }
}

// Execute the test
runTest().catch(console.error);