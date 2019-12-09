import React, { Component } from 'react'
import './App.css'
import TodoList from './TodoList'
import { Row, Col } from 'antd'
import { Layout } from 'antd';
const { Header, Content } = Layout;

class App extends Component {

  render() {
    return (
      <div>
        <Layout>
          <Header></Header>
          <Content>
            <div>
              <Row>
                <Col span={12} offset={6}>
                  <h1><center>Welcome to LC-Group</center></h1>
                </Col>
              </Row>
              <Row>
                <Col xs={2} sm={4} md={4} lg={4} xl={4}>
                </Col>
                <Col xs={20} sm={16} md={16} lg={16} xl={16}>
                  <div className="App">
                    <TodoList />
                  </div>
                </Col>
                <Col xs={2} sm={4} md={4} lg={4} xl={4}>
                </Col>
              </Row>
            </div>
          </Content>
        </Layout>
      </div>
    )
  }
}
export default App