// Mandatory Imports
import React, {useState, useEffect} from 'react';
import './App.css';
// Layouts
import axios from 'axios'; // REST API requests

// Internal Component Imports
import ResponsiveAppBar from './components/MenuBar';
import TableDraggableRow from './components/TableDraggableRow';
import { TextField } from '@mui/material';
import Button from "@mui/material/Button";
import Grid from '@mui/material/Unstable_Grid2';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import Highlight from 'react-highlight';
import { Scrollbar } from 'react-scrollbars-custom';
import Autocomplete from '@mui/material/Autocomplete';
import { JsonEditor as Editor, JsonEditor } from "jsoneditor-react";
import "jsoneditor-react/es/editor.min.css";
import Modal from '@mui/base/Modal';
import Typography from '@mui/material/Typography';
import Backdrop from '@mui/material/Backdrop';
import ace from 'brace';
import 'brace/mode/json.js';
import 'brace/theme/github.js';
import Divider from '@mui/material/Divider';
// Custom Components
import VirtualizedList from './components/VirtualizedList';
import JobList from './components/JobList';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: "70vw",
  height: "80vh",
  borderRadius:"5px",
  bgcolor: 'background.paper',
  border: '1px solid #fff',
  boxShadow: 2,
  p: 4,
};

function App() {
  const [height, setHeight] = useState(4);
  const [queueName, setQueueName] = useState("demorack");
  const [data, setData] = useState("None");
  const queueurl = `http://localhost:5000/queue-dict/${queueName}`
  const queueurlnames = `http://localhost:5000/queue_names`
  const test_plan_req_url = `http://localhost:5000/get_test_plan_paths`
  const [mlock, setMlock] = useState(0); // this lock is used to stop updates
  const [time, setTime] = useState(0);
  const [updateFreq, setUpdateFreq] = useState(300);
  const [showList, setShowList] = useState(1);
  const [listContents, setListContents] = useState([{'id':'','name':""}]);
  const [customTestPlan, setCustomTestPlan] = useState({"Example":"Hello World"});


  const [showHelp, setShowHelp] = useState(false);

const [customDict, setCustomDict] = useState({
  "TEST_NAME":{
      "TP::skip":"no",
      "TP::test_plan_name":"TEST_NAME",
  }
});

const [testPlanList, setTestPlanList] = useState([]);
const [testPlanPath, setTestPlanPath] = useState("");
const [storedTestPlan, setStoredTestPlan] = useState("none");

  // Modal
  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

    // Modal2
    const [open2, setOpen2] = useState(false);
    const handleOpen2 = () => setOpen2(true);
    const handleClose2 = () => setOpen2(false);

      // Modal3
      const [open3, setOpen3] = useState(false);
      const handleOpen3 = () => setOpen3(true);
      const handleClose3 = () => setOpen3(false);

  let defaultList = [
    {label:"demorack"}
  ]
  const [queueNames, setQueueNames] = useState(
    defaultList
  )
  useEffect(() => {
    const interval = setInterval(() => {
      //console.log(mlock);
      //console.log(updateFreq);
      if (mlock == 0) {
        //console.log("NEW UPDATED!");
        setTime(new Date());
        setUpdateFreq(3000);
      } else {
        //console.log("BYPASS TIME UPDATE");
      }
    }, updateFreq);
    return () => {
      //console.log("Cleaning interval");
      clearInterval(interval);
    }
  });
  
  useEffect(() => {
    axios.get(queueurl).then((response)=> {setData(JSON.stringify(response.data,null,4));set_data(response.data);determineShowList(response.data)}).catch(function(error){console.log(error);setData("Unknown");setShowList(0);setListContents([{'id':'','name':""}])})
  }
  ,[queueName, height, time]);

  useEffect(() => {
    axios.get(queueurlnames).then((response)=> {setQueueNames(response.data);console.log("Setting queue name list")}).catch(function(error){console.log(error);setQueueNames(defaultList);})
  }
  ,[queueName, height]);

  useEffect(() => {
    axios.get(test_plan_req_url).then((response)=> {setTestPlanList(response.data);}).catch(function(error){console.log(error);setTestPlanList([]);})
  }
  ,[testPlanPath]);

  function determineShowList(listItems) {
    if (listItems.length == 0) {
      setShowList(0);
    } else if (listItems == []) {
      setShowList(0);
    } else {
      setShowList(1);
    }
  }

  function set_data(datagram) {
    //console.log("T5")
    //console.log(datagram)
    if(datagram.length == 0) {
      //console.log("Test1");
      setListContents([{'id':'','name':""}]);
    } else {
      //console.log("Test2");
      setListContents(datagram);
    }
  }
  function sendRequest(suburl) {
    console.log("SENDING!");
    axios.get("http://localhost:5000/"+suburl).catch(function(error){console.log(error);});
    setUpdateFreq(300);
    decrementCount();
  }
  console.log(mlock);
  function decrementCount() {
      setHeight(prevHeight => prevHeight -1 );
  }

  function sendCustomDict() {
    handleClose();
    console.log(JSON.stringify(customDict));
    axios.get("http://localhost:5000/add?name="+queueName + "&data="+JSON.stringify(customDict)).catch(function(error){console.log(error);});
    setUpdateFreq(300);
  }

  function sendStoredDict(test_plan_path) {
    setUpdateFreq(300);
    axios.get("http://localhost:5000/add_test_plan?name="+queueName + "&json_path="+JSON.stringify(test_plan_path)).catch(function(error){console.log(error);});
    setUpdateFreq(300);
  }
  
  // FOR EXTRACTING JSON INFORMATION FROM SERVER
  function sendTestPlan() {
    handleClose2();
    console.log(JSON.stringify(customTestPlan));
    axios.get("http://localhost:5000/add?name="+queueName + "&data="+JSON.stringify(customTestPlan)).catch(function(error){console.log(error);});
    setUpdateFreq(300);
  }

  function queryTestPlan(query) {
    let testplantquery = "http://localhost:5000/get_test_plan?name="+query;
    console.log(testplantquery);
    //axios.get(test_plan_req_url).then((response)=> {setTestPlanList(response.data);}).catch(function(error){console.log(error);setTestPlanList([]);})
  }

  const switch1 = { inputProps: { 'aria-label': 'Switch demo' } };
  


  return (
    <>
    <ResponsiveAppBar openModal={handleOpen3}/>
    <br></br>
    {/*<h6>{data}</h6>*/}
    
    <Grid container spacing={2} columns={16}>
        <Grid xs={3} sx={{"background":"#f4f4f4","border":"1px solid white","borderRadius":"5px"}}>
        <Typography variant="button" display="block" gutterBottom>
            Active Queues 
          </Typography>
          <Divider/>
        <Scrollbar style={{ width: "100%", height: "80vh",  }} scrollbarWidth={20}>
          <VirtualizedList sx={{overflowX:"hidden"}} data={queueNames} setQueueName={setQueueName}></VirtualizedList>
          </Scrollbar>
        </Grid>
        <Grid xs={7}>
          {/*<a href={"http://localhost:5000/queue/"+queueName}> <Button  size="small" variant="outlined">Go to Queue Manager</Button></a>{" "}
          <Button onClick={() => sendRequest("populate2?name="+queueName)}  size="small" variant="outlined">Add Demo</Button>{" "}
          <Button onClick={() => sendRequest("add_test_plan?name="+queueName+"&json_name=ppa3_master")}  size="small" variant="outlined">Add PPA3</Button>{" "}*/}
          <Button onClick={handleOpen2} color="success" size="small" variant="outlined">+ Import Test</Button>{" "}
          <Button onClick={handleOpen} color="success" size="small" variant="outlined">+ Add Custom Dictionary</Button>{" "}
          <Button onClick={() => {sendRequest("clear?name="+queueName)}}  color="error" size="small" variant="outlined">Clear Queue</Button>
          
          <h1></h1>
          {/*<h1>Queue Name: {queueName}</h1>*/}
          
          
          <Modal open={open} onClose={handleClose} aria-labelledby="modal-modal-title" aria-describedby="modal-modal-description" slots={{ backdrop: Backdrop }}>
          
          <Box sx={style}>
          <Typography id="modal-modal-title" variant="h6" component="h2">
            Add a Custom Dictionary to Queue
          </Typography>
          <Typography id="modal-modal-description" sx={{ mt: 2 }}>
            Copy and paste your json here to append it to the end of the current queue ({queueName}).
          </Typography>
          <Editor
            mode="text"
            value={customDict}
            onChange={(content) => {
              setCustomDict(content);
            }}
            ace={ace}
            theme="ace/theme/github"
          ></Editor><Button onClick={sendCustomDict} color="success" variant="contained" sx={{float:"right",margin:"10px"}}>+ Add to Queue</Button>{" "}
        </Box>
          </Modal>

            {/* THIS MODAL IS FOR IMPORT TEST*/}
          <Modal open={open2} onClose={handleClose2} aria-labelledby="modal-modal-title" aria-describedby="modal-modal-description" slots={{ backdrop: Backdrop }}>
          
          <Box sx={style}>
          {JSON.stringify(testPlanList)}
        </Box>
          </Modal>


          <Autocomplete
            disablePortal
            id="combo-box-demo"
            onOpen={() => {decrementCount();console.log(height);}}
            options={queueNames}
            sx={{ width: 300 }}
            inputValue={queueName}
            value={queueName}
            
            onInputChange={(event, newInputValue) => {
              console.log("CHANGINED!");
              setQueueName(newInputValue);
            }}
            renderInput={(params) => <TextField {...params} label="Queue Name" />}
          />
          {/*<TextField id="outlined-basic" label="Queue Name" variant="outlined" defaultValue={queueName} 
          onChange={(event)=> setQueueName(event.target.value)}/>*/}
          <br></br>
          {showList == 1 ? (
            <Scrollbar style={{ width: "100%", height: "70vh" }} scrollbarWidth={20}>
          {/*<div style={{ display: 'inline-flex', overflowY: 'scroll', height:'100%', maxHeight:"70vh"}}>*/}
          <TableDraggableRow name={queueName} data2={listContents} setMlock={setMlock} setUpdateFreq={setUpdateFreq} decrementCount={decrementCount}></TableDraggableRow>
          {/*</div>*/}</Scrollbar>):(queueName !== "" ? (<div> <Alert severity="info">
          <AlertTitle>Do you want to create a new queue? ({queueName})</AlertTitle><br></br>
          This queue is currently empty.  Click on the buttons below to add demo tests, or use the Test Planner to push tests to this queue.<br></br><br></br>
          <Button onClick={() => sendRequest("populate2?name="+queueName)}  size="small" variant="contained">Add Dummy Tests (small)</Button>{" "}
          <Button onClick={() => sendRequest("add_test_plan?name="+queueName+"&json_name=ppa3_master")}  size="small" variant="contained">Add PPA3 Tests (large)</Button>{" "}<br></br>
        </Alert>
        </div>):(<div> <Alert severity="warning">
          <AlertTitle>The queue name cannot be empty</AlertTitle><br></br>
          Please enter a valid queue name in the search bar above.
        </Alert>
        </div>))
          }
          {/*<h6>Data Refresh Rate: {updateFreq/1000}s</h6>*/}
        </Grid>
        <Grid xs={6} sx={{"background":"#f4f4f4","border":"1px solid white","borderRadius":"5px"}}>
        <Modal open={open3} onClose={handleClose3} slots={{ backdrop: Backdrop }}>
        
        <Box sx={style}>
          <Alert severity="success">
          <AlertTitle>REST API for Accessing This Queue's Items</AlertTitle>
          <a href={"http://localhost:5000/queue-dict/"+queueName}>http://localhost:5000/queue-dict/{queueName}</a>
        </Alert>
        <Alert severity="success">
          <AlertTitle>API Docs</AlertTitle>
          All other REST API commands for controlling this queue can be found here: 
          <a href="http://localhost:5000/docs"> http://localhost:5000/docs</a>
        </Alert>
        <Alert severity="info">
          <AlertTitle>What are Dictionary Priority Queues?</AlertTitle>
          Dictionary priority queues are dictionaries ordered by a priority number (rank). These queues are stored using <a href="https://redis.io/docs/data-types/sorted-sets/#:~:text=A%20Redis%20sorted%20set%20is,Leaderboards.">redis sorted sets</a>.
          program consumes dictionaries to run tests, therefore the dictionary priority queue acts
          as a serverless scheduler for <strong>dynamically queueing and re-ordering </strong>tests.
        </Alert>
        
        <Alert severity="info">
          <AlertTitle>Instructions how to use</AlertTitle>
          <h5>Step 1: Set up the DPQ client onto your SUT</h5>
          Run the following script in command line (CLI): <br></br>

          This client will listen to all queues based on names.  SUTs will be listening to the queue name defined by environmental variable JENKINS_LABEL.  
          To add additional queues to listen to, add queue names to the environmental variable SCHEDULER_LABELS (seperated by commas).  
          <Highlight language="javascript">
              {`SCHEDULER_LABELS="localhost_a3,nv32_xl"`}
          </Highlight>
          <h5>Step 2: Add tests to the queue using Test Planner</h5>
          Use the "Queue" button instead of the "Run" button to submit the job to the Dictionary Priority Queue.<br></br>
          <h5>Step 3: View/Modify the queue</h5>
          To view the queue items, type in the queue name to the "Queue Name" text box on the right.<br></br>
          Here, you can delete, modify the dictionary, and reorder the dictionary through drag/drop.
        </Alert>
        </Box>
        </Modal>
        
        <Typography variant="button" display="block" gutterBottom>
            Add Stored Dictionaries
          </Typography>
          <Divider/>
        <Scrollbar style={{ width: "100%", height: "80vh",  }} scrollbarWidth={20}>
          <JobList sx={{overflowX:"hidden"}} data={testPlanList} setQueueName={setQueueName} sendStoredDict={sendStoredDict}></JobList>
          </Scrollbar>
        
        </Grid>
    </Grid>
    </>
  );
}

export default App;