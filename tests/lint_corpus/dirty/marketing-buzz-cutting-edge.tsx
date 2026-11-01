const features = [{ title: "Routing", body: "Built on cutting-edge research." }];
export const List = () => <ul>{features.map((f) => <li key={f.title}>{f.body}</li>)}</ul>;
