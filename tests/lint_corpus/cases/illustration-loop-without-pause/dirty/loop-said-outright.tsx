import { Stage } from './stageshow'

export function Card() {
  return <Stage width={400} height={300} play="loop" script={async (a) => { await a.wait(3000) }}>{() => null}</Stage>
}
