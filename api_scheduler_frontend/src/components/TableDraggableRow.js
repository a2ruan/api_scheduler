import React, { Component, useState } from "react";
import ReactDOM from "react-dom";
import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";
import Paper from "@mui/material/Paper"; // List of Jobs
import Stack from "@mui/material/Stack"; // Card spacing
import { List } from "@mui/material";

export default function TableDraggableRow(name) {
    let name4 = "hello"
    console.log("preprint")
    console.log(name)
    if (name) {
        console.log("STARTING")
        name4 = name.name;
        console.log(name4)
    }


    let randomList = [
    {
      id: "Andy",
      name: name4,
    },
    {
      id: "Cindy",
      name: "Cindy Ruan",
    },
    {
      id: "Shally",
      name: "Shally Guo",
    },
    {
      id: "Michael",
      name: "Michael Ruan",
    },
    {
      id: "Tina",
      name: "Tina Kong",
    },
  ];

  const [characters, updateCharacters] = useState(randomList);

  function handleOnDragEnd(result) {
    // Saves state of list
    if (!result.destination) return;
    const items = Array.from(characters);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);
    updateCharacters(items);
  }

  return (
    <div>
      <DragDropContext onDragEnd={handleOnDragEnd}>
        <Droppable droppableId="table1">
          {(provided, snapshot) => (

            <ul
              className="characters"
              {...provided.droppableProps}
              ref={provided.innerRef}
            >
              <div>
                <ul className="hello no-bullets">
                  <Stack spacing={1}>
                    {characters.map(({ id, name }, index) => {
                      return (
                        <Draggable key={id} draggableId={id} index={index}>
                          {(provided) => (
                            <li
                              {...provided.draggableProps}
                              {...provided.dragHandleProps}
                              ref={provided.innerRef}
                            >
                              <div className="characters-thumb">
                                <Paper elevation={5}>
                                  {name} 
                                    <br></br>
                                    Order={index}
                                </Paper>
                              </div>
                            </li>
                          )}
                        </Draggable>
                      );
                    })}
                    {provided.placeholder}
                  </Stack>
                </ul>
              </div>
            </ul>
          )}
        </Droppable>
      </DragDropContext>
    </div>
  );
}
