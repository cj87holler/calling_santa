import { RealtimeSession } from '@openai/agents/realtime';
import { agent } from './agent';

const btn = document.getElementById('start-btn')!;

btn.addEventListener('click', async () => {
  const session = new RealtimeSession(agent);

  await session.connect({
    apiKey: import.meta.env['VITE_OPENAI_API_KEY'],
  });

  btn.textContent = 'Listening...';
});