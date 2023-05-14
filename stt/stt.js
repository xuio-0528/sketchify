const { Configuration, OpenAIApi } = require("openai");
const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);
const resp = await openai.createTranscription(
  fs.createReadStream("audio.mp3"),
  "whisper-1"
);

// response는 아래와 같은 형식으로 나타납니다.
// {
//   "text": "Imagine the wildest idea that you've ever had, and you're curious about how it might scale to something that's a 100, a 1,000 times bigger. This is a place where you can get to do that."
// }
