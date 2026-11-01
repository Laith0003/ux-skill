export const A = () => (
  <>
    <Input placeholder="No label prop" />
    <Input label="" placeholder="Empty label" />
    <Input label={undefined} placeholder="Undefined label" />
    <Input label="Email" placeholder="you@x.com" />
    <InputGroup placeholder="Group" />
  </>
);
