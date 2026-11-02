import { Stage, Window } from './stageshow'

export function Hero() {
  return (
    <section>
      <h2>Send invoices in a minute</h2>
      <Stage width={720} height={340}>
        {() => (
          <Window url="billing.acme.studio">
            <div className="title">Invoices</div>
          </Window>
        )}
      </Stage>
    </section>
  )
}
