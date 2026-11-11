# Voz de los reels (elegida por Iñaki el 11-11-2026)

- Motor: Gemini TTS (Google AI Studio, capa gratis). Se llama desde Apps Script (propiedad `GEMINI_KEY`), porque la nube de los agentes no llega a la API.
- Voz: **Finn** (voz prediseñada gratis, "Warm and approachable").
- Estilo (pegar tal cual como instrucción de estilo):

> Acento chileno (español de Chile), narrador viral de reels: más animado y con chispa, sonriendo al hablar, mucho entusiasmo y energía alta pero natural, ritmo ágil, como un creador de contenido chileno joven que cuenta un dato curioso que lo emociona

- Escribir los números en palabras ("veinticinco kilos") y el sitio como "basesegura punto cl".
- En guion.json: `"voz": "gemini:Finn"`. Mientras no esté conectado, queda Kokoro como respaldo.
