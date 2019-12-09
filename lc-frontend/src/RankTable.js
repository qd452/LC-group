import React, { Component } from "react";
import { Table } from 'antd';

class RankTable extends Component {
    constructor(props) {
        super(props)
        this.state = {
            students: [
                { id: 1, name: 'Wasif', age: 21, email: 'wasif@email.com' },
                { id: 2, name: 'Ali', age: 19, email: 'ali@email.com' },
                { id: 3, name: 'Saad', age: 16, email: 'saad@email.com' },
                { id: 4, name: 'Asad', age: 25, email: 'asad@email.com' }
            ],
            columns: [
                {
                    title: 'Name',
                    dataIndex: 'name',
                    key: 'name',
                },
                {
                    title: 'Age',
                    dataIndex: 'age',
                    key: 'age',
                },
                {
                    title: 'Email',
                    dataIndex: 'email',
                    key: 'email',
                }
            ],
        }
    }

    renderTableHeader() {
        let header = Object.keys(this.state.students[0])
        return header.map((key, index) => {
            return <th key={index}>{key.toUpperCase()}</th>
        })
    }

    renderTableData() {
        return this.state.students.map((student, index) => {
            const { id, name, age, email } = student //destructuring
            return (
                <tr key={id}>
                    <td>{id}</td>
                    <td>{name}</td>
                    <td>{age}</td>
                    <td>{email}</td>
                </tr>
            )
        })
    }

    render() {
        var tableEntries = this.props.entries;
        console.log(tableEntries);
        if (tableEntries) {
            let ranCol = [
                {
                    title: 'Rank',
                    dataIndex: 'rank',
                    key: 'rank',
                },
                {
                    title: 'Name',
                    dataIndex: 'name',
                    key: 'name',
                },
                {
                    title: 'Score',
                    dataIndex: 'score',
                    key: 'score',
                },
                {
                    title: 'Finish_time',
                    dataIndex: 'finish_time',
                    key: 'finish_time',
                }
            ];

            let user_ranks = [];
            console.log(tableEntries.user_ranks);
            for (let i = 0; i < tableEntries.user_ranks.length; i++) {
                let userRank = tableEntries.user_ranks[i];
                console.log(userRank);
                user_ranks.push({
                    'rank': userRank.rank.rank,
                    'name': userRank.rank.username,
                    'score': userRank.rank.score,
                    'finish_time': userRank.rank.finish_time
                })
            }

            return (
                <div>
                    {/* <h1 id='title'>Dummy Table</h1>
                    <Table dataSource={this.state.students} columns={this.state.columns} /> */}

                    <h1 id='title'>{tableEntries.contest_num}</h1>
                    <Table dataSource={user_ranks} columns={ranCol} />
                </div>
            )
        }
        return <div></div>
    }
}

export default RankTable;