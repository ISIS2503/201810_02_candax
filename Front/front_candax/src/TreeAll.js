import React, { Component } from 'react';
import axios from 'axios'
import Tree from 'react-d3-tree';
import Navbar from './Navbar'
import Conventions from './Conventions'
import {Panel} from 'react-bootstrap';
import Websocket from 'react-websocket';


const myTreeData = [
  {
    name: 'Parent Node',
    nodeSvgShape: {
      shape: 'circle',
      shapeProps: {
        r: 10,
        fill: '#04B4AE'
      }
    }
  }
];

const containerStyles = {
  width: '100%',
  height: '60%'
}

class TreeAll extends Component {

  constructor(){
    super()
    this.state ={
      data: myTreeData,
      house: 'Seleccione una casa',
      name:'',
      last_name:'',
      res_unit:'',
      email:''
    }

    var newData = []
    var dataFinal =[]
    axios.get('http://localhost:8000/tree').then(response => {newData= response.data[0]['data']; dataFinal.push(newData); this.setState({data: dataFinal});})
  }

  componentDidMount() {
    const dimensions = this.treeContainer.getBoundingClientRect();
    this.setState({
      translate: {
        x: dimensions.width / 2,
        y: dimensions.height / 14
      }
    });
  }

  handleData(data) {
    var newData = data
    var dataFinal =[]
    dataFinal.push(JSON.parse(newData))
    this.setState({data: dataFinal});
  }

  render() {
    return (
      <div style={{width: '100%', height: '100%'}}>
        
        <Navbar/>
        
        <div style={containerStyles} ref={tc => (this.treeContainer = tc)}>
         <Tree data={this.state.data} orientation = 'vertical' translate={this.state.translate} onClick= {function a(nodeData, evt)
                                                                                                                    {
                                                                                                                      if(nodeData.name.startsWith("H")){
                                                                                                                          axios.get('http://localhost:8000/house_detail' + nodeData.name).then(response => {
                                                                                                                            this.setState({name: response.data.name});
                                                                                                                            this.setState({last_name: response.data.last_name});
                                                                                                                            this.setState({email: response.data.email});
                                                                                                                            this.setState({res_unit: response.data.res_unit});
                                                                                                                            this.setState({house: response.data.house});
                                                                                                                          })
                                                                                                                        }
                                                                                                                    }.bind(this)
                                                                                                                  }/>
        </div>
        {/* <div id = "holaaaaaaawi">
         <MiModal/>
        </div> */}
          <Conventions/>
        <div>
            <Panel>
              <Panel.Heading>Casa: {this.state.house}</Panel.Heading>
              <Panel.Body>
              Nombre: {this.state.name}
              <hr/>
              Apellido: {this.state.last_name}
              <hr/>
              Email: {this.state.email}
              <hr/>
              Unidad Residencial: {this.state.res_unit}
              </Panel.Body>
            </Panel>
        </div>
        <Websocket url='ws://localhost:8000/socket' onMessage={this.handleData.bind(this)}/>
      </div>
    );
  }
}

  export default TreeAll;
