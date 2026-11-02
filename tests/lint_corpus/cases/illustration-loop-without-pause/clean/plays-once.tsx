import { Stage } from './stageshow'

export function Hero() {
  return <Stage width={720} height={340} play="once" script={async (a) => { await a.wait(3000) }}>{() => null}</Stage>
}
