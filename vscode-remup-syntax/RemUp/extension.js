/**
 * RemUp VSCode Extension - Main Entry Point
 * Provides complete support for RemUp markup language
 * 
 * Features:
 * - Syntax highlighting
 * - Auto word wrap (like Markdown)
 * - Smart editing
 * - Code snippets
 */

const vscode = require('vscode');

/**
 * Activate the extension
 * @param {vscode.ExtensionContext} context - Extension context
 */
function activate(context) {
    console.log('RemUp extension is now active!');
    
    // Apply default settings for RemUp files
    applyRemupSettings();
    
    // Listen for configuration changes
    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration(e => {
            if (e.affectsConfiguration('remup')) {
                applyRemupSettings();
            }
        })
    );
    
    // Register command to toggle word wrap
    const toggleWordWrapCommand = vscode.commands.registerCommand('remup.toggleWordWrap', () => {
        const config = vscode.workspace.getConfiguration('remup');
        const currentValue = config.get('enableAutoWrap', true);
        config.update('enableAutoWrap', !currentValue, vscode.ConfigurationTarget.Global);
        vscode.window.showInformationMessage(`RemUp auto word wrap ${!currentValue ? 'enabled' : 'disabled'}`);
    });
    
    context.subscriptions.push(toggleWordWrapCommand);
}

/**
 * Apply editor settings for RemUp files
 */
function applyRemupSettings() {
    const config = vscode.workspace.getConfiguration('remup');
    
    // Get user configurations
    const enableAutoWrap = config.get('enableAutoWrap', true);
    const wordWrapColumn = config.get('wordWrapColumn', 120);
    
    // Update workspace settings
    const workspaceConfig = vscode.workspace.getConfiguration();
    
    // Apply settings for RemUp language
    if (enableAutoWrap) {
        workspaceConfig.update(
            '[remup]',
            {
                'editor.wordWrap': 'on',
                'editor.wrappingIndentation': 'same',
                'editor.renderWhitespace': 'selection'
            },
            vscode.ConfigurationTarget.Workspace
        );
    }
}

/**
 * Deactivate the extension
 */
function deactivate() {
    console.log('RemUp extension deactivated');
}

module.exports = {
    activate,
    deactivate
};