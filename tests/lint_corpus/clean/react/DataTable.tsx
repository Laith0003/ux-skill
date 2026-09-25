import { Box, Table, TableBody, TableCell, TableHead, TableRow } from "../ui/table";
import type { Shipment } from "./types";

type Props = {
  rows: Shipment[];
  stickyOffset: number;
  onSelect: (id: string) => void;
};

/*
 * The sx objects below use theme spacing units, not pixels: p: 2 is two
 * spacing steps. Nothing here sets zIndex: 9999 or width: 100vw; the sticky
 * header offset is measured at runtime.
 */
export function ShipmentTable({ rows, stickyOffset, onSelect }: Props) {
  return (
    <Box
      sx={{
        p: 2,
        borderRadius: 1,
        bgcolor: "background.paper",
        overflowX: "auto",
        maxInlineSize: "100%",
      }}
    >
      <Table aria-label="Shipments due this week" size="small">
        <TableHead
          sx={{
            position: "sticky",
            top: stickyOffset,
            zIndex: "var(--z-sticky)",
            "& th": { fontWeight: 600, color: "text.secondary" },
          }}
        >
          <TableRow>
            <TableCell>Reference</TableCell>
            <TableCell>Destination</TableCell>
            <TableCell align="right">Pallets</TableCell>
            <TableCell>Status</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow
              key={row.id}
              hover
              sx={{
                "&:last-child td": { borderBottom: 0 },
                "&:focus-visible": { outline: "2px solid", outlineColor: "primary.main" },
              }}
            >
              <TableCell>
                <button type="button" className="link-button" onClick={() => onSelect(row.id)}>
                  {row.reference}
                </button>
              </TableCell>
              <TableCell>{row.destination}</TableCell>
              <TableCell align="right" sx={{ fontVariantNumeric: "tabular-nums" }}>
                {row.pallets}
              </TableCell>
              <TableCell>
                <Box component="span" sx={{ px: 1, py: 0.25, borderRadius: 1, fontSize: 13 }}>
                  {row.statusLabel}
                </Box>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Box>
  );
}
