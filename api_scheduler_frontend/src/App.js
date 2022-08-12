// Mandatory Imports
import React from 'react';
import './App.css';

// Layouts


import axios from 'axios'; // REST API requests

// Internal Component Imports
import BasicExampleDataGrid from './components/DeviceTable';
import FullWidthGrid from './components/FullWidthGrid';
import ResponsiveAppBar from './components/MenuBar';
import TableDraggableRow from './components/TableDraggableRow';

function App() {

  let randomList = [
    {
      id: "Andy",
      name: "Andy Ruan",
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

  return (
    <>
    <ResponsiveAppBar/>
    <h1></h1>
    <FullWidthGrid/>
    <TableDraggableRow/>
    </>
    // <div>
    //     <>
    //       <h1>Hello world</h1>
    //       <BasicExampleDataGrid></BasicExampleDataGrid>
        
    //     <h1>Hello world</h1>
    //       <BasicExampleDataGrid></BasicExampleDataGrid>
    //     </>
    // </div>
  );
}

export default App;

// export default class App extends React.Component {
  
//   constructor(props) {
//     super(props);
//     this.state = {
//       data: []
//     };
//   }

//   componentDidMount() {
//     // This function retrieves dictionary info from a get request
//     axios.get('http://mkm-l10-andyru9:5000/room-list')
//     .then(response => {
//         console.log(typeof(response.data))
//         const data = response.data;
//         this.setState({ data })
//       })
//       .catch(error => {
//         console.log(error);
//       })
//     this.timer = setInterval(() => {
//       axios.get('http://mkm-l10-andyru9:5000/room-list')
//     .then(response => {
//         console.log(typeof(response.data))
//         const data = response.data;
//         this.setState({ data })
//       })
//       .catch(error => {
//         console.log(error);
//       })
      
//       // code to refresh your component.
//     },1000)
//   }

//   componentWillUnmount() {
//     clearInterval(this.timer);
//   }

//   render() {

//     return (
//       <div>
//         {this.state.data.hello}
//         <p></p>Unit testing for TableFilterable {2+2}
//       </div>
//     );
//   }
// }