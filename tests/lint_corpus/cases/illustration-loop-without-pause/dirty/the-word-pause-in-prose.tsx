import { Stage } from './stageshow'

export function Hero() {
  return (
    <section>
      <Stage width={720} height={340} script={async (a) => { await a.wait(3000) }}>{() => null}</Stage>
      <p>Take a pause</p>
      <video src="/clip.mp4" onPause={() => {}} />
    </section>
  )
}
