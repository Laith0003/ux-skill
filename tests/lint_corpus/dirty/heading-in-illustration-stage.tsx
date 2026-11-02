import { Stage, Window } from './stageshow'

export function Hero() {
  return (
    <Stage width={720} height={340}>
      {() => (
        <Window url="billing.acme.studio">
          <h3 className="title">Invoices</h3>
        </Window>
      )}
    </Stage>
  )
}
