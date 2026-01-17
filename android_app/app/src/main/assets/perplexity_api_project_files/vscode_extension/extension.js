
const vscode = require('vscode');
const axios = require('axios');

function getConfig() {
    const config = vscode.workspace.getConfiguration('perplexityBridge');
    return {
        url: config.get('url', 'http://localhost:7860'),
        apiKey: config.get('apiKey', 'dev-secret'),
        model: config.get('model', 'mistral-7b-instruct')
    };
}

function activate(ctx) {
    let cmd = vscode.commands.registerCommand('perplexity.ask', async () => {
        try {
            // Get user input
            const query = await vscode.window.showInputBox({
                prompt: 'Enter your question for Perplexity',
                placeHolder: 'What would you like to know?'
            });
            
            if (!query) {
                return; // User cancelled
            }
            
            // Get configuration
            const config = getConfig();
            
            if (!config.url || !config.apiKey) {
                vscode.window.showErrorMessage(
                    'Perplexity Bridge configuration is missing. Please set perplexityBridge.url and perplexityBridge.apiKey in settings.'
                );
                return;
            }
            
            // Show progress
            await vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: 'Asking Perplexity...',
                cancellable: false
            }, async (progress) => {
                try {
                    // Make API request
                    const response = await axios.post(
                        `${config.url}/v1/chat/completions`,
                        {
                            model: config.model,
                            messages: [{ role: 'user', content: query }]
                        },
                        {
                            headers: {
                                'X-API-KEY': config.apiKey,
                                'Content-Type': 'application/json'
                            },
                            timeout: 60000 // 60 second timeout
                        }
                    );
                    
                    // Validate response
                    if (!response.data || !response.data.choices || !response.data.choices[0]) {
                        throw new Error('Invalid response format from API');
                    }
                    
                    const content = response.data.choices[0].message.content;
                    
                    if (!content) {
                        throw new Error('Empty response from API');
                    }
                    
                    // Show response
                    vscode.window.showInformationMessage(content, 'Copy').then(selection => {
                        if (selection === 'Copy') {
                            vscode.env.clipboard.writeText(content);
                            vscode.window.showInformationMessage('Response copied to clipboard');
                        }
                    });
                    
                    // Also show in output channel
                    const outputChannel = vscode.window.createOutputChannel('Perplexity Bridge');
                    outputChannel.appendLine(`Query: ${query}`);
                    outputChannel.appendLine(`Response: ${content}`);
                    outputChannel.appendLine('---');
                    outputChannel.show();
                    
                } catch (error) {
                    let errorMessage = 'Failed to connect to Perplexity Bridge';
                    
                    if (error.response) {
                        // API returned error response
                        errorMessage = `API Error: ${error.response.status} - ${error.response.statusText}`;
                        if (error.response.data && error.response.data.error) {
                            errorMessage += ` - ${error.response.data.error}`;
                        }
                    } else if (error.request) {
                        // Request made but no response
                        errorMessage = 'No response from Perplexity Bridge. Is the server running?';
                    } else if (error.message) {
                        errorMessage = `Error: ${error.message}`;
                    }
                    
                    vscode.window.showErrorMessage(errorMessage);
                    console.error('Perplexity Bridge error:', error);
                }
            });
            
        } catch (error) {
            vscode.window.showErrorMessage(`Unexpected error: ${error.message}`);
            console.error('Unexpected error:', error);
        }
    });
    
    ctx.subscriptions.push(cmd);
}

exports.activate = activate;
