export const A = () => (
  <>
    <div role="presentation" onClick={go}>x</div>
    <div role="none" onClick={go}>x</div>
    <div role="button" tabIndex={0} onClick={go}>x</div>
    <div role={"button"} onClick={go}>x</div>
  </>
);
