import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { requestAPI } from './handler';

/**
 * Initialization data for the jupyter-server-titiler extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyter-server-titiler:plugin',
  description: 'A Jupyter server extension providing a TiTiler server.',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension jupyter-server-titiler is activated!');

    requestAPI<any>('get-example')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The jupyter_server_titiler server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
