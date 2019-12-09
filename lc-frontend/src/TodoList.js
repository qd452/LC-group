import React, { Component } from "react"; 
// import TodoItems from "./TodoItems";
import RankTable from "./RankTable";
const axios = require('axios');
import { AutoComplete, Button } from 'antd';

const dataSource = ['weekly-contest-', 'biweekly-contest-'];



class TodoList extends Component { 
  constructor(props) {    
    super(props);     

    this.state = { 
      contest_rank: null
    };

    this.addItem = this.addItem.bind(this);
  }

  async getUserRanking(contest_num) {
    try {
      const response = await axios.get('api/v0/contest/ranking/' + contest_num);
      // console.log(response);
      this.setState({
        contest_rank: response.data
      });
    } catch (error) {
      console.error(error);
    }  
  }

  addItem(e) {
    console.log('addItem');
    if (this._inputElement !== "") {
      let contest_num = this._inputElement;  
      this.getUserRanking(contest_num); 
    }     
    e.preventDefault();
  }


  render() {    
    return (      
      <div className="todoListMain">        
        <div className="header">          
          {/* <form onSubmit={this.addItem}>            
            <input ref={(a) => this._inputElement = a} 
              placeholder="weekly-contest-165">
            </input> 
            <button type="submit">add</button>          
          </form>         */}
          <AutoComplete
            style={{ width: 200 }}
            dataSource={dataSource}
            placeholder=""
            filterOption={(inputValue, option) =>
              option.props.children.toUpperCase().indexOf(inputValue.toUpperCase()) !== -1
            }
            onSearch={value => {
              this._inputElement = value;
              // console.log(value, this._inputElement);
            }}
          />

          <Button type="primary" icon="search" onClick={this.addItem}>
            Go
          </Button>

        </div>

        <RankTable entries={this.state.contest_rank}/>  
        {/* <TodoItems entries={this.state.contest_rank}/> */}
      </div>    
    );  
  }
} 

export default TodoList;