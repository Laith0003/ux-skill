export function PhoneField() {
  return (
    <label>
      Phone
      <input type="tel" name="phone" pattern="[+]962 ?7[789]\d{7}" />
    </label>
  );
}
