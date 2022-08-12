import * as React from "react";
import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";

import BasicExampleDataGrid from "./DeviceTable";
import TableDraggableRow from "./TableDraggableRow";
// const Item = styled(Paper)(({ theme }) => ({
//   backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
//   ...theme.typography.body2,
//   padding: theme.spacing(1),
//   textAlign: 'center',
//   color: theme.palette.text.secondary,
// }));

export default function FullWidthGrid() {
  return (
    <Box sx={{ flexGrow: 12 }}>
      <Grid container spacing={1}>
        <Grid item xs={2} md={2}>
        <TableDraggableRow name="helloTT"/>
          
        </Grid>
        <Grid item xs={6} md={6}>
        <BasicExampleDataGrid />
        </Grid>
        <Grid item xs={4} md={4}>
          <BasicExampleDataGrid />
        </Grid>
      </Grid>
    </Box>
  );
}
