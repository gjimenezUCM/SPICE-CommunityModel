// Creado a partir del archivo de configuración de Pedro Pablo Gómez (PadaOne)
// Muchos de los comentarios son directamente suyos
//
// Configuración de WebPack 'en release'. Se empaqueta todo el código
// en un bundle, de modo que se puede lanzar de forma autónoma sin
// instalar dependencias de Node.
//
// Esto permite hacer un contenedor con un node sin npm, y no tener que
// hacer un npm install previo durante la build (así evitamos toda la sobrecarga).
// que generan los node_modules


const path = require('path');

// Plugin para limpiar el directorio de la build antes de cada recompilación.
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CopyPlugin = require("copy-webpack-plugin");
const { node } = require('webpack');

module.exports = {
    mode: 'production',
    target: 'node',
  // Si el código compilado usa las 'variables de node'
  // __dirname y __filename, que devuelven el directorio y
  // nombre del fichero donde se usan, al hacer la build
  // no funcionará. Al fin y al cabo, la build fusiona todo
  // en el mismo fichero y la cosa termina fallando. Si
  // es importante que se mantengan los valores originales
  // entonces hay que configurar WebPack para que lo haga.
  // (https://webpack.js.org/configuration/node/#node-__dirname)
  //
  // Como mucho, lo normal será que en el código solo uses
  // __dirname para saber dónde estás y moverte buscando algún
  // otro fichero con recursos. Esos recursos deberían ser cosas
  // distintas a código JavaScript (o TypeScript) porque eso lo
  // cargarás con import. Lo normal será que uses __dirname al
  // hacer una aplicación con Express/Koa donde uses ficheros
  // HTML o similar que sirvas a los clientes, y que tendrás cerca
  // junto al empaquetado generado con WebPack.
  // node: {
  //   // WebPack, por favor, conserva los __dirname y __filename
  //   // originales. Si no, serán vacíos o '/'.
  //   // https://stackoverflow.com/questions/57797709/webpack-fs-readfilesync-inside-a-node-modules-dependency
  //   global: true,
  //   __dirname: true,   // if you don't put this is, __dirname
  //   __filename: true,  // and __filename return blank or /
  // },
    entry: {
      app: './index.js'
    },
    resolve: {
      // Si se importa algún fichero, sin indicar extensión,
      // prueba con las siguientes.
      extensions: ['.js']
    },

    plugins: [
      new CopyPlugin({
        patterns: [
          { 
            from: 'api',
            to: 'api',
            context: "app/"
          },
           // {
           //   from: 'node_modules/swagger-ui-dist/',
           //   to: 'node_modules/swagger-ui-dist/'
           // }
        ],
      }),
      // Limpiamos el directorio destino. 
      new CleanWebpackPlugin( /*[path.resolve(__dirname, 'dist')]*/),
    ],
    output: {
      filename: 'main.js',
      path: path.resolve(__dirname, 'build'),
    },
  };