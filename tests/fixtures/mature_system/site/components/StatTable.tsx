export function StatTable({ rows }) {
  return (
    <table className="font-data">
      <tbody>
        <tr><td className="font-data tabular-nums">{rows[0]}</td></tr>
      </tbody>
    </table>
  );
}
