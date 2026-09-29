export const A = () => <input type="tel" pattern={"\\+[0-9]{8,}"} />;
export const B = () => <input type={"tel"} pattern="[0-9]{9,10}" />;
export const C = () => <input type="tel" pattern={phonePattern} />;
