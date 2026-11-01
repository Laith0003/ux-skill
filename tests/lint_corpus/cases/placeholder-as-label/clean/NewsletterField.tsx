import { useId } from "react";

export function NewsletterField() {
  const id = useId();
  return (
    <div className="field">
      <label htmlFor={id}>Email</label>
      <input id={id} type="email" placeholder="you@company.com" />
      <label htmlFor="coupon">Coupon</label>
      <input id="coupon" type="text" placeholder="Optional" />
    </div>
  );
}
