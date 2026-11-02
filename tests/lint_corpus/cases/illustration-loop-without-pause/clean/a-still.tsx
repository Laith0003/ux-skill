import { Stage, Window } from './stageshow'

export function Card() {
  return <Stage width={400} height={300}>{() => <Window url="acme.studio" />}</Stage>
}
