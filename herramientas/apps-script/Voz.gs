/**
 * Voz de los reels con Gemini TTS (voz Finn, acento chileno animado).
 *
 * Cómo funciona:
 *  1. El agente de contenido (nube) manda un correo a basesegura.cl@gmail.com con asunto
 *     "VOZ PEDIDO AAAA-MM-DD" y en el cuerpo un JSON: {"fecha":"AAAA-MM-DD","escenas":["texto 1","texto 2",...]}
 *  2. procesarPedidosVoz() (activador cada 5 minutos) genera un .wav por escena con Gemini,
 *     los junta en voz.zip y responde en el mismo hilo con asunto "VOZ LISTA AAAA-MM-DD".
 *  3. El agente descarga voz.zip y arma el reel.
 *
 * La clave va en Propiedades de la secuencia de comandos como GEMINI_KEY (nunca en el código).
 * Instalar: pegar este archivo en el proyecto "Contenido", guardar y ejecutar instalarVoz() una vez.
 */

var VOZ_NOMBRE = 'Finn';
var VOZ_MODELO = 'gemini-3.8-flash-tts';
var VOZ_ESTILO = 'Acento chileno (español de Chile), narrador viral de reels: más animado y con chispa, ' +
  'sonriendo al hablar, mucho entusiasmo y energía alta pero natural, ritmo ágil, como un creador de ' +
  'contenido chileno joven que cuenta un dato curioso que lo emociona';
var VOZ_API = 'https://generativelanguage.googleapis.com/v1beta/';
var VOZ_ETIQUETA = 'Voz hecha';

function instalarVoz() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'procesarPedidosVoz') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('procesarPedidosVoz').timeBased().everyMinutes(5).create();
  Logger.log('Activador listo. Prueba: ' + probarVoz());
}

/** Genera una frase de prueba y la manda a tu correo para escucharla. */
function probarVoz() {
  var wav = vozEscena_('¿Sabías que en Chile la ley limita a veinticinco kilos la carga que un trabajador puede levantar a mano? Esto te interesa.');
  wav.setName('prueba-finn.wav');
  GmailApp.sendEmail(Session.getEffectiveUser().getEmail(), 'Prueba voz Finn', 'Escucha el adjunto.', { attachments: [wav] });
  return 'ok, revisa tu correo (' + wav.getBytes().length + ' bytes)';
}

function procesarPedidosVoz() {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(1000)) return;
  try {
    var etiqueta = GmailApp.getUserLabelByName(VOZ_ETIQUETA) || GmailApp.createLabel(VOZ_ETIQUETA);
    var hilos = GmailApp.search('subject:"VOZ PEDIDO" -label:"' + VOZ_ETIQUETA + '" newer_than:3d', 0, 5);
    var inicio = Date.now();
    hilos.forEach(function (hilo) {
      if (Date.now() - inicio > 4 * 60 * 1000) return;
      var msj = hilo.getMessages()[0];
      var pedido = JSON.parse(msj.getPlainBody().trim().replace(/^[^{]*/, '').replace(/[^}]*$/, ''));
      var carpeta = carpetaPedido_(pedido.fecha);
      for (var i = 0; i < pedido.escenas.length; i++) {
        var nombre = ('0' + i).slice(-2) + '.wav';
        if (carpeta.getFilesByName(nombre).hasNext()) continue;  // ya hecha en una pasada anterior
        if (Date.now() - inicio > 4.5 * 60 * 1000) return;       // sigue en la próxima pasada
        var wav = vozEscena_(pedido.escenas[i]);
        wav.setName(nombre);
        carpeta.createFile(wav);
      }
      var blobs = [];
      for (var j = 0; j < pedido.escenas.length; j++) {
        blobs.push(carpeta.getFilesByName(('0' + j).slice(-2) + '.wav').next().getBlob());
      }
      var zip = Utilities.zip(blobs, 'voz.zip');
      hilo.replyAll('Voz ' + VOZ_NOMBRE + ' lista: ' + blobs.length + ' escenas.', {
        subject: 'VOZ LISTA ' + pedido.fecha, attachments: [zip]
      });
      hilo.addLabel(etiqueta);
      carpeta.setTrashed(true);
    });
  } finally {
    lock.releaseLock();
  }
}

function carpetaPedido_(fecha) {
  var nombre = 'voz-reel-' + fecha;
  var it = DriveApp.getFoldersByName(nombre);
  return it.hasNext() ? it.next() : DriveApp.createFolder(nombre);
}

function idVoz_() {
  var props = PropertiesService.getScriptProperties();
  var id = props.getProperty('VOZ_ID');
  if (id) return id;
  var r = llamar_('get', 'voices?search=' + encodeURIComponent(VOZ_NOMBRE) + '&page_size=50');
  var voces = r.voices || [];
  var v = voces.filter(function (x) { return (x.display_name || x.displayName || x.id) === VOZ_NOMBRE; })[0];
  id = v ? v.id : VOZ_NOMBRE;
  props.setProperty('VOZ_ID', id);
  return id;
}

function vozEscena_(texto) {
  var cuerpo = {
    model: VOZ_MODELO,
    input: [{
      type: 'user_input',
      content: [{ type: 'text', text: texto, annotations: [{ type: 'speech_metadata', style: VOZ_ESTILO }] }]
    }],
    response_format: { type: 'audio', mime_type: 'audio/wav' },
    generation_config: { speech_config: [{ voice: idVoz_() }] }
  };
  for (var intento = 0; intento < 4; intento++) {
    try {
      var r = llamar_('post', 'interactions', cuerpo);
      var datos = buscarAudio_(r);
      if (!datos) throw new Error('Sin audio en la respuesta: ' + JSON.stringify(r).slice(0, 300));
      var bytes = Utilities.base64Decode(datos);
      if (String.fromCharCode(bytes[0], bytes[1], bytes[2], bytes[3]) !== 'RIFF') bytes = conCabeceraWav_(bytes, 24000);
      return Utilities.newBlob(bytes, 'audio/wav');
    } catch (e) {
      if (!/429|RESOURCE_EXHAUSTED|500|503/.test(String(e)) || intento === 3) throw e;
      Utilities.sleep(25000);
    }
  }
}

function llamar_(metodo, ruta, cuerpo) {
  var clave = PropertiesService.getScriptProperties().getProperty('GEMINI_KEY');
  if (!clave) throw new Error('Falta GEMINI_KEY en Propiedades de la secuencia de comandos');
  var op = { method: metodo, headers: { 'x-goog-api-key': clave }, muteHttpExceptions: true };
  if (cuerpo) { op.contentType = 'application/json'; op.payload = JSON.stringify(cuerpo); }
  var res = UrlFetchApp.fetch(VOZ_API + ruta, op);
  var codigo = res.getResponseCode();
  if (codigo >= 300) throw new Error(codigo + ' ' + res.getContentText().slice(0, 500));
  return JSON.parse(res.getContentText());
}

function buscarAudio_(o) {
  if (!o || typeof o !== 'object') return null;
  if (o.type === 'audio' && o.data) return o.data;
  if (o.output_audio && o.output_audio.data) return o.output_audio.data;
  var ks = Object.keys(o), hallado = null;
  for (var i = 0; i < ks.length; i++) {
    var d = buscarAudio_(o[ks[i]]);
    if (d) hallado = d;  // se queda con el último bloque de audio
  }
  return hallado;
}

function conCabeceraWav_(pcm, sr) {
  var h = [], n = pcm.length;
  function s(t) { for (var i = 0; i < t.length; i++) h.push(t.charCodeAt(i)); }
  function u32(v) { h.push(v & 255, (v >> 8) & 255, (v >> 16) & 255, (v >> 24) & 255); }
  function u16(v) { h.push(v & 255, (v >> 8) & 255); }
  s('RIFF'); u32(36 + n); s('WAVE'); s('fmt '); u32(16); u16(1); u16(1); u32(sr); u32(sr * 2); u16(2); u16(16);
  s('data'); u32(n);
  return h.map(function (b) { return b > 127 ? b - 256 : b; }).concat(pcm);
}
