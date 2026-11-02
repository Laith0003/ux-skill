import { Stage, Window } from './stageshow'

export function Hero() {
  return (
    <Stage width={720} height={340} initial={{ sent: false }}
      script={async (a) => { await a.click('send'); a.set({ sent: true }); await a.wait(2000) }}>
      {() => <Window url="billing.acme.studio" />}
    </Stage>
  )
}
