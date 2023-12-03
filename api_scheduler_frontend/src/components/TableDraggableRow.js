import React, { useState, useEffect } from "react";
import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";
import Paper from "@mui/material/Paper"; // List of Jobs
import Stack from "@mui/material/Stack"; // Card spacing
import axios from "axios";
import { JsonEditor as Editor, JsonEditor } from "jsoneditor-react";
import "jsoneditor-react/es/editor.min.css";
import Button from "@mui/material/Button";
import Chip from "@mui/material/Chip";
import Avatar from "@mui/material/Avatar";
import DragIndicatorIcon from '@mui/icons-material/DragIndicator';
const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 700,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

export default function TableDraggableRow(name) {
  // MODAL
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const [characters, updateCharacters] = useState(name.data2);
  const [currentId, setCurrentId] = useState("None"); // used to identify current edited element
  const [counter, updateCounter] = useState(0);

  let queueName = name.name;

  useEffect(() => {
    updateCounter((prevCounter) => prevCounter + 1);
    updateCharacters(name.data2);
  }, [name.data2]);

  function handleOnDragStart(result) {
    //console.log("STARTL");
    //console.log(name.handler);
    name.setMlock(1);
    name.setUpdateFreq(600);
    console.log("ENDL");
  }

  function handleOnDragEnd(result) {
    if (!result.destination) {
      //console.log("Did not relocate!");
      name.setMlock(0);
      name.setUpdateFreq(300);
      return;
    }

    const items = Array.from(characters);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);
    updateCharacters(items);
    const queueurl = `http://localhost:5000/drag?name=${
      name.name
    }&source_index=${result.source.index.toString()}&target_index=${result.destination.index.toString()}`;
    const queueurl2 = `http://localhost:5000/swap?name=${
      name.name
    }&source_index=${result.source.index.toString()}&target_index=${result.destination.index.toString()}`;
    //console.log(queueurl);
    if (
      result.source.index - result.destination.index == 1 ||
      result.destination.index - result.source.index == 1
    ) {
      axios.get(queueurl2).catch(function (error) {
        console.log(error);
      });
    } else if (result.source.index != result.destination.index) {
      axios.get(queueurl).catch(function (error) {
        console.log(error);
      });
    }
    name.setMlock(0);
    name.setUpdateFreq(300);
  }

  function sendRequest(suburl) {
    name.setUpdateFreq(300);
    console.log("SENDING!");
    console.log(suburl);
    axios.get("http://localhost:5000/" + suburl).catch(function (error) {
      console.log(error);
    });
    name.setUpdateFreq(300);
  }

  function callback_jsoneditor(content, id) {
    console.log("Callback!");
    let url_edit = `edit?name=${name.name}&id=${id}&obj=${JSON.stringify(
      content
    )}`;
    console.log(url_edit);
    console.log("ENDL");
    sendRequest(url_edit);
    return () => {};
  }

  function toggleEditor(id) {
    console.log("toggling!");
    console.log(id);
    var x = document.getElementById("Modal" + id);
    console.log(x);
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }

  // Avatar Rendering

  function stringToColour(str) {
    let new_str = "";
    if (str.split("_").length > 0) {
      new_str = str.substring(str.indexOf('_')+1);
      str = new_str
    }
    //console.log(new_str);
    var hash = 0;
    str.split("").forEach((char) => {
      hash = char.charCodeAt(0) + ((hash << 5) - hash);
    });
    let colour = "#";
    for (let i = 0; i < 3; i++) {
      var value = (hash >> (i * 8)) & 0xff;
      colour += value.toString(16).padStart(2, "0");
    }
    //let replacement = "5"
    //colour = colour.substring(0, 1) + replacement + colour.substring(1 + replacement.length);

    let replacement = "7"
    colour = colour.substring(0, 3) + replacement + colour.substring(3 + replacement.length);

    return colour;
  }

  function editorEvent(event) {
    //console.log("Editor Event!");
    //console.log(event);
  }

  return (
    <div>
      {/*counter}--{currentId*/}
      <DragDropContext
        onDragEnd={handleOnDragEnd}
        onDragStart={handleOnDragStart}
      >
        <Droppable droppableId="table1">
          {(provided) => (
            <ul
              className="characters"
              {...provided.droppableProps}
              ref={provided.innerRef}
            >
              <div>
                <ul className="hello no-bullets">
                  <Stack spacing={1}>
                    {characters.map(({ id, name, json}, index) => {
                      return (
                        <Draggable
                          key={id}
                          draggableId={id}
                          index={index}>
                          {(provided) => (
                            <li>
                              <div className="characters-thumb"
                              {...provided.draggableProps}
                              {...provided.dragHandleProps}
                              ref={provided.innerRef}>
                                <Paper
                                  elevation={2}
                                  variant="outlined"
                                  sx={{
                                    bgcolor:
                                      stringToColour(
                                        name
                                      ) + "20",
                                      paddingBottom:"4px"
                                  }}
                                ><DragIndicatorIcon color="disabled" sx={{transform:"translateY(6px)"}}></DragIndicatorIcon>
                                
                                  <Chip 
                                    variant="rounded"
                                    onClick={(event) => {
                                      toggleEditor(id);
                                      editorEvent(event, id, );
                                    }}
                                    sx={{ 
                                      textTransform: "uppercase",
                                      bgcolor:
                                        stringToColour(
                                          name
                                        ) + "30",
                                      color: stringToColour(
                                        name
                                      ),
                                      fontWeight: "bolder",
                                      fontSize:"12px"
                                    }}
                                    avatar={
                                      <Avatar
                                        sx={{
                                          bgcolor: stringToColour(
                                            name
                                          ),
                                        }}
                                      >
                                        <strong>
                                          <font size="+0.5" color="white">
                                            {index + 1}
                                          </font>
                                        </strong>
                                      </Avatar>
                                    }
                                    label={name}
                                  ></Chip>
                                  <Button
                                    sx={{"float":"right"}}
                                    onClick={() => {
                                      sendRequest(
                                        "rem?name=" +
                                          queueName +
                                          "&index=" +
                                          index.toString()
                                      );
                                    }}
                                    color="error"
                                    size="small"
                                  >
                                    Delete
                                  </Button>
                                  <Button
                                    onClick={(event) => {
                                      toggleEditor(id);
                                      editorEvent(event, id, );
                                    }}
                                    size="small"
                                    sx={{"float":"right"}}
                                  >
                                    Edit
                                  </Button>
                                  <div
                                    id={"Modal" + id}
                                    style={{ display: "none" }}
                                  >
                                    <Editor 
                                      mode="text"
                                      value={json}
                                      
                                      onChange={(content) => {
                                        callback_jsoneditor(content, id);
                                      }}
                                    ></Editor>
                                  </div>
                                  {/*<br></br>
                                  Order={index}*/}
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
