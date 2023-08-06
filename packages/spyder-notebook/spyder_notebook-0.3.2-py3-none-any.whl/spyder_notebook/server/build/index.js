// Copyright (c) Jupyter Development Team, Spyder Project Contributors.
// Distributed under the terms of the Modified BSD License.
import { PageConfig, URLExt } from '@jupyterlab/coreutils';
// @ts-ignore
__webpack_public_path__ = URLExt.join(PageConfig.getBaseUrl(), 'example/');
import '@jupyterlab/application/style/index.css';
import '@jupyterlab/codemirror/style/index.css';
import '@jupyterlab/completer/style/index.css';
import '@jupyterlab/notebook/style/index.css';
import '@jupyterlab/tooltip/style/index.css';
if (PageConfig.getOption('darkTheme') == 'true') {
    require('@jupyterlab/theme-dark-extension/style/index.css');
    require('../dark-theme-hack.css');
}
else {
    require('@jupyterlab/theme-light-extension/style/index.css');
}
import '../index.css';
import { CommandRegistry } from '@phosphor/commands';
import { MenuBar, SplitPanel, Widget } from '@phosphor/widgets';
import { ServiceManager } from '@jupyterlab/services';
import { MathJaxTypesetter } from '@jupyterlab/mathjax2';
import { NotebookPanel, NotebookWidgetFactory, NotebookModelFactory } from '@jupyterlab/notebook';
import { CompleterModel, Completer, CompletionHandler, KernelConnector } from '@jupyterlab/completer';
import { editorServices } from '@jupyterlab/codemirror';
import { DocumentManager } from '@jupyterlab/docmanager';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { RenderMimeRegistry, standardRendererFactories as initialFactories } from '@jupyterlab/rendermime';
import { SetupCommands } from './commands';
function main() {
    let manager = new ServiceManager();
    void manager.ready.then(() => {
        createApp(manager);
    });
}
function createApp(manager) {
    // Initialize the command registry with the bindings.
    let commands = new CommandRegistry();
    let useCapture = true;
    // Setup the keydown listener for the document.
    document.addEventListener('keydown', event => {
        commands.processKeydownEvent(event);
    }, useCapture);
    let rendermime = new RenderMimeRegistry({
        initialFactories: initialFactories,
        latexTypesetter: new MathJaxTypesetter({
            url: PageConfig.getOption('mathjaxUrl'),
            config: PageConfig.getOption('mathjaxConfig')
        })
    });
    let opener = {
        open: (widget) => {
            // Do nothing for sibling widgets for now.
        }
    };
    let docRegistry = new DocumentRegistry();
    let docManager = new DocumentManager({
        registry: docRegistry,
        manager,
        opener
    });
    let mFactory = new NotebookModelFactory({});
    let editorFactory = editorServices.factoryService.newInlineEditor;
    let contentFactory = new NotebookPanel.ContentFactory({ editorFactory });
    let wFactory = new NotebookWidgetFactory({
        name: 'Notebook',
        modelName: 'notebook',
        fileTypes: ['notebook'],
        defaultFor: ['notebook'],
        preferKernel: true,
        canStartKernel: true,
        rendermime,
        contentFactory,
        mimeTypeService: editorServices.mimeTypeService
    });
    docRegistry.addModelFactory(mFactory);
    docRegistry.addWidgetFactory(wFactory);
    let notebookPath = PageConfig.getOption('notebookPath');
    let nbWidget = docManager.open(notebookPath);
    // Create menu bar.
    let menuBar = new MenuBar();
    menuBar.addClass('notebookMenuBar');
    const editor = nbWidget.content.activeCell && nbWidget.content.activeCell.editor;
    const model = new CompleterModel();
    const completer = new Completer({ editor, model });
    const connector = new KernelConnector({ session: nbWidget.session });
    const handler = new CompletionHandler({ completer, connector });
    // Set the handler's editor.
    handler.editor = editor;
    // Listen for active cell changes.
    nbWidget.content.activeCellChanged.connect((sender, cell) => {
        handler.editor = cell && cell.editor;
    });
    // Hide the widget when it first loads.
    completer.hide();
    // Create panel with menu bar above the notebook widget
    let panel = new SplitPanel();
    panel.id = 'main';
    panel.orientation = 'vertical';
    panel.spacing = 0;
    SplitPanel.setStretch(menuBar, 0);
    SplitPanel.setStretch(nbWidget, 1);
    panel.addWidget(menuBar);
    panel.addWidget(nbWidget);
    // Attach the panel to the DOM.
    Widget.attach(panel, document.body);
    Widget.attach(completer, document.body);
    // Handle resize events.
    window.addEventListener('resize', () => {
        panel.update();
    });
    SetupCommands(commands, menuBar, nbWidget, handler);
}
window.addEventListener('load', main);
//# sourceMappingURL=index.js.map