import React from "react";
import {Button, Media, Tab, Tabs, Nav} from 'react-bootstrap';
import Edit  from "./EditProfile"
import { connect } from 'react-redux';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';


const option = {
  onRowClick: function(row, columnIndex, rowIndex) {
    console.log(row)
    alert(`You click row id: ${row.game_name}, column index: ${columnIndex}, row index: ${rowIndex}`);
  },
};


@connect((store) => {
	return {
		user: store.user.user,
		gamelist: store.user.game_list,
		wishlist: store.user.wish_list,
		fetched: store.user.fetched,
	};
})

export default class Profile extends React.Component {
	constructor(props){
		super(props);
		this.state= {
            isedit: false,
		};
		this.requestedit = this.requestedit.bind(this);
	}

	requestedit(){
		this.setState({ isedit: true });
	}

	imageFormatter(cell,row){
        return (
            <img style={{height:35}} src={cell}/>
        )
    };


	render () {
		if (this.state.isedit){
			return (
			<Edit />
			);
		}

		//get the profile data from backend
		const { user,fetched } = this.props;
		console.log(fetched);
		if(fetched) {
			//get data
			console.log(user.user_name);
			return(
			<div>
					<div className ="media-left">
						<img src = "http://www.ravalyogimatrimony.com/Content/images/default-profile-pic.png" alt = "profile picture"/>
					</div>
					<div className = "media-body">
					<p> Username : {user.user_name} </p>
    				<Button className = "btn btn-primary" type ="submit"  name = "Submit" onClick={this.requestedit}>Edit</Button>
    				</div>
    				<Tabs defaultActiveKey={1} className="String" id="uncontrolled-tab-example">
    					<Tab eventKey={1} title="Playlist">
    						<div>
    						    <BootstrapTable data={this.props.gamelist} options={ option } hover pagination>
                                    <TableHeaderColumn dataField='image_url' dataFormat={this.imageFormatter} width = '90px' ></TableHeaderColumn>
                                    <TableHeaderColumn isKey dataField='game_name' >Game Name</TableHeaderColumn>
                                </BootstrapTable>
    						</div>
    					</Tab>
   						<Tab eventKey={2} title="Wishlist">
   						    <div>
    						    <BootstrapTable data={this.props.wishlist} options={ option } hover pagination>
                                    <TableHeaderColumn dataField='image_url' dataFormat={this.imageFormatter} width = '90px' ></TableHeaderColumn>
                                    <TableHeaderColumn isKey dataField='game_name' >Game Name</TableHeaderColumn>
                                </BootstrapTable>
    						</div>
   						</Tab>
   					</Tabs>
			</div>
			);
		}
	}
}
