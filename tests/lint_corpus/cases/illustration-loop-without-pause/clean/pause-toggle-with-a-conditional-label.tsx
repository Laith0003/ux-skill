import { useState } from 'react'
import { Stage } from './stageshow'

export function Hero() {
  const [paused, setPaused] = useState(false)
  return (
    <div>
      <Stage width={720} height={340} script={async (a) => { await a.wait(3000) }}>{() => null}</Stage>
      <button type="button" aria-label={paused ? 'Play' : 'Pause'} onClick={() => setPaused(!paused)}>||</button>
    </div>
  )
}
