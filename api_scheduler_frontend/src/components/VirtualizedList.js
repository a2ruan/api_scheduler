import React from "react";
import { FixedSizeList } from "react-window";
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Badge from '@mui/material/Badge';
import WorkIcon from '@mui/icons-material/Work';
import { styled } from '@mui/material/styles';
const StyledBadge = styled(Badge)(({ theme }) => ({
  '& .MuiBadge-badge': {
    right: -3,
    top: 13,
    border: `2px solid ${theme.palette.background.paper}`,
    padding: '0 4px',
  },
}));

export default function VirtualizedList(input) {
  //const itemsArray = ["a","b","c"]; // our data
  let itemsArray = [{"label":"a"},{"label":"b"},{"label":"c"}]; // our data
  itemsArray = input.data
  const Row = ({ index, style }) => (
    <ListItem style={style} key={index} component="div" disablePadding className={index % 2 ? "ListItemOdd" : "ListItemEven"}>
      <ListItemButton onClick={() =>{console.log(itemsArray[index].label);input.setQueueName(itemsArray[index].label)}}>
      <Badge badgeContent={itemsArray[index].queue_size} color="primary">
        <WorkIcon color="action" fontSize="small"/>
      </Badge>
        <ListItemText sx={{"paddingLeft":"20px"}} primary={itemsArray[index].label} />
      </ListItemButton>
        
    </ListItem>

  );
 
  return (
    
  <FixedSizeList
    className="List"
    height={(itemsArray.length+1)*(35)}
    itemCount={itemsArray.length}
    itemSize={35}
    width={250}
  >
    {Row}    
  </FixedSizeList>

  
  );

};