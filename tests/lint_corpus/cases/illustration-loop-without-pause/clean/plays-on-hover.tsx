import { Stage } from './stageshow'

export function Tile() {
  return <Stage width={400} height={300} play='hover' script={async (a) => { await a.wait(3000) }}>{() => null}</Stage>
}
