import React from "react";
import {Button, Media, Tab, Tabs, Nav} from 'react-bootstrap';
import Edit  from "./EditProfile"
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import { getRecommendation2,getFollowList,getRecommendation1, edit_hrs,updatepprofile  } from '../../actions/userActions';

@connect((store) => {
	return {
		user: store.user.user,
		wishlist: store.user.wish_list,
    gamelist: store.user.game_list,
		fetched: store.user.fetche,
	};
})

export default class Profile extends React.Component {
	constructor(props){
		super(props);
		this.state= {
		    rec1:[],
		    follow_list: [],
		    rec2:[],
        gamelist:[],
        top_genres:[],
		};
		this.requestedit = this.requestedit.bind(this);
    this.SaveCell = this.SaveCell.bind(this);
	}

	requestedit(){
		this.setState({ isedit: true });
	}

	nameFormatter(cell,row,enumObject, index){
        return (
            <div>
                <Link className='game_name' to ={{
                    pathname: `/games/${row.game_id}`,
                    state: {index}
                }}>
                {cell}
                </Link>
            </div>
    )
  }

  profileFormatter(cell,row,enumObject, index){
        return (
            <div>
                <Link className='user_name' to ={{
                    pathname: `/profiles/${row.user_name}`,
                }}>
                {cell}
                </Link>
            </div>
    )
  }



  componentWillMount() {
    const username=this.props.user.user_name;
    console.log("rec run");
    updatepprofile(username)
        .then((res)=>{
          console.log("dfdfdf",res.data);
          this.setState({
            gamelist: res.data.gamelist,
          })
    })
    getRecommendation1(username)
        .then((res)=>{
            console.log(res.data)
            this.setState({
            rec1: res.data.results,
            top_genres:res.data.top_genres,
          })
        })
    getFollowList(username)
        .then((res)=>{
            this.setState({
            follow_list: res.data.follows,
            })
         })
    getRecommendation2(username)
        .then((res)=>{
            this.setState({
            rec2: res.data.results,
          })
        })

    }


	imageFormatter(cell,row){
        return (
            <img style={{height:35}} src={cell}/>
        )
    };

  SaveCell(row, cellName, cellValue){
      edit_hrs(row.game_id,this.props.user,cellValue)
	}

  onBeforeSaveCell(row, cellName, cellValue) {
    // You can do any validation on here for editing value,
    // return false for reject the editing
		if(cellValue.match(/\D+/g)){
			alert("please only input number");
			return false
		}
    return true;
  }



	render () {
    console.log(this.state.rec1);
		if (this.state.isedit){
			return (
			<Edit />
			);
		}

    const cellEditProp = {
      mode: 'click',
      blurToSave: true,
			beforeSaveCell:this.onBeforeSaveCell,
      afterSaveCell: this.SaveCell  // a hook for after saving cell
    };
		//get the profile data from backend
    console.log(this.state.gamelist);
		const { user,fetched } = this.props;
		if(fetched) {
			return(
			<div>
					<div className ="media-left">
						<img src = "http://www.ravalyogimatrimony.com/Content/images/default-profile-pic.png" alt = "profile picture"/>
					</div>
					<div className = "media-body">
					<p> Username : {user.user_name} </p>
    				<Button className = "btn btn-primary" type ="submit"  name = "Submit" onClick={this.requestedit}>Edit</Button>
    				</div>
						<div className='page-tabs'>
    				<Tabs defaultActiveKey={1} className="Tabulation" id="uncontrolled-tab-example">
    					<Tab eventKey={1} title="Playlist">
    						<div>
                  {this.props.gamelist.length> 0 ? (this.state.gamelist.length> 0 ? (<BootstrapTable data={this.state.gamelist} hover pagination cellEdit={ cellEditProp }>
                    <TableHeaderColumn dataField='thumbnail' dataFormat={this.imageFormatter} width = '90px' editable={false}></TableHeaderColumn>
                    <TableHeaderColumn isKey dataField='game_name'  dataFormat={this.nameFormatter} width='200px'>Game Name</TableHeaderColumn>
                    <TableHeaderColumn  editable={ { type: 'textarea'}} dataField='played_hrs' width='120px'>Played Hours (Click number to edit)</TableHeaderColumn>
                  </BootstrapTable>):
                    (<img src='static/images/loading.svg' height="50" width="50"/>)):
                    (<div>There is no game in your game list</div>)}
    						</div>
    					</Tab>
   						<Tab eventKey={2} title="Wishlist">
   						    <div>
    						    <BootstrapTable data={this.props.wishlist} hover pagination>
                                    <TableHeaderColumn dataField='thumbnail' dataFormat={this.imageFormatter} width = '90px' ></TableHeaderColumn>
                                    <TableHeaderColumn isKey dataField='game_name'  dataFormat={this.nameFormatter} width='300px'>Game Name</TableHeaderColumn>
                                </BootstrapTable>
    						</div>
   						</Tab>
   						<Tab eventKey={3} title="Popular Recommendation">
   						    <div>
                    <strong>there are some popular genres that you usually play {this.state.genre_list}</strong>
    						    <BootstrapTable data={this.state.rec1} hover>
                        <TableHeaderColumn dataField='image_url' dataFormat={this.imageFormatter} width = '90px' ></TableHeaderColumn>
                        <TableHeaderColumn isKey dataField='game_name'  dataFormat={this.nameFormatter} width='300px'>Game Name</TableHeaderColumn>
                        <TableHeaderColumn dataField='genre_list'>Genres</TableHeaderColumn>
                    </BootstrapTable>
    						</div>
   						</Tab>
   						<Tab eventKey={4} title="Our Recomendation">
   						    <div>
    						    <BootstrapTable data={this.state.rec2} hover>
                                    <TableHeaderColumn dataField='image_url' dataFormat={this.imageFormatter} width = '90px' ></TableHeaderColumn>
                                    <TableHeaderColumn isKey dataField='game_name'  dataFormat={this.nameFormatter} width='300px'>Game Name</TableHeaderColumn>
                    </BootstrapTable>
    						</div>
   						</Tab>
   						<Tab eventKey={5} title="Follow List">
   						    <div>
    						    <BootstrapTable data={this.state.follow_list} hover pagination>
                                    <TableHeaderColumn isKey dataField='user_name' dataFormat={this.profileFormatter}  width='300px'>Username</TableHeaderColumn>
                                    <TableHeaderColumn dataField='num_games'  width='300px'>Number of Games</TableHeaderColumn>
                                </BootstrapTable>
    						</div>
   						</Tab>
   					</Tabs>
						</div>
			</div>
			);
		}
		return null;
	}
}
