**
 * @author Tyler Werman
 */

import java.util.ArrayList;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Orientation;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.ScrollPane;
import javafx.scene.control.TextField;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.FlowPane;
import javafx.scene.layout.TilePane;
import javafx.scene.layout.VBox;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.scene.text.Text;

public class SearchView{
	Scene searchScene;
	final int HEIGHT = 600;
	final int WIDTH = 1000;
	final int IMAGE_HEIGHT = 150;
	final int FLOWPANE_WIDTH = 700;
	final int HGAP = 20;
	TextField search = new TextField();
	ArrayList<ImageView> recPlants=new ArrayList<>();
	ArrayList<FlowPane> fps=new ArrayList<>();
	ComboBox<String> comboBox;
/**
 * A constructor to build the searchScene that the SearchView holds.	
 * @param c The controller of the whole program that can grab information from the model and give it to the view.
 */
	public SearchView(Controller c) {
		//Create border pane, the root of the scene
		BorderPane mainPane = new BorderPane();
		mainPane.setPrefHeight(HEIGHT);
		mainPane.setPrefWidth(WIDTH);
		
		//Create tile pane that will hold the search bar at the top of the borderpane
		TilePane searchPane = createTP(c);
		mainPane.setTop(searchPane);
		
		//Create the scrollpane of different plants held in the center of the borderpane
		VBox vb = new VBox();
		ScrollPane plantList = new ScrollPane();
		vb.getChildren().add(plantList);
		plantList.setContent(vb);
		addToSP(plantList,c,vb);
		mainPane.setCenter(plantList);
		
		//Create the flowpane that will allow the user to sort the plants on the right of the 
		//borderpane
		FlowPane sortOption = createSidePane();
		mainPane.setRight(sortOption);
		
		//Create a back button to get back to the plot on the left of the borderpane
		Button backButton = new Button("Back");
		backButton.setOnAction(e->c.moveOnePageBack(e));
		mainPane.setLeft(backButton);
		searchScene = new Scene(mainPane);
	}
	/**
	 * Creates the tile pane that will allow the user to search through the available plants
	 * @param c The overarching controller of the project that allows the view to use eventhandlers and get info from model transfered
	 * through controller
	 * @return	the tile pane that will allow a user to search through plants by name
	 */
	public TilePane createTP(Controller c) {
		TilePane searchPane = new TilePane();
		Button searchButton = new Button("Search");
		search.setPromptText("Search Plants Here");
		searchPane.getChildren().addAll(search,searchButton);
		searchPane.setAlignment(Pos.CENTER);
		return searchPane;
	}
	
	/**
	 * Creates a scrollpane for the available plants so the user can search through every plant the 
	 * program offers.
	 * @param sp the scrollpane holding the vbox
	 * @param c The overarching controller of the project that allows the view to use eventhandlers and get info from model transfered
	 * through controller
	 * @param v the vbox that holds all of the flowpanes with pictures and text for each plant
	 */
	public void addToSP(ScrollPane sp, Controller c,VBox v) {
		//Creates an array list of imageviews for each plant in the program
		for (int i=0;i<c.ap.size();i++) {
			//creates and imageview for each plant in the available plants
			ImageView j=new ImageView(new Image(c.ap.get(i).getImagePath()));
			j.setPreserveRatio(true);
	    	j.setFitHeight(IMAGE_HEIGHT);
			recPlants.add(j);
			
			//Creates a flowpane for each plant with a picture and their name
			FlowPane plantPane = createFlowPane(c,c.ap.get(i),j);
			fps.add(plantPane);
			v.getChildren().add(fps.get(i));
		}
		//tracks the scrollpane's vertical value (received from https://docs.oracle.com/javafx/2/ui_controls/scrollpane.htm)
		sp.vvalueProperty().addListener(new ChangeListener<Number>() {
		    public void changed(ObservableValue<? extends Number> ov,
		        Number old_val, Number new_val) {
		            v.setLayoutY(-new_val.doubleValue());
		        }
		});
	}
	
	/**
	 * Creates a flowpane holding a pictures a names for each plant the program offers
	 * @param c The overarching controller of the project that allows the view to use eventhandlers and get info from model transfered
	 * through controller
	 * @param p The plant that the flow pane will hold information about
	 * @param j The imageview of the plant 
	 * @return	A flowpane holding an image of the a plant, the common and scientific name of the plant, and a button for more info 
	 */
	public FlowPane createFlowPane(Controller c,Plants p,ImageView j) {
		//Creates a new flowpane and assigns its size and orientation
		FlowPane fp = new FlowPane(Orientation.HORIZONTAL);
		fp.setPrefWidth(FLOWPANE_WIDTH);
		fp.setAlignment(Pos.CENTER_LEFT);
		fp.setHgap(HGAP);
		
		//Create and texts and a button
		Text plantNames = new Text(p.getName()+"\n\n"+p.getScientificName());
		plantNames.setFont(Font.font("Verdana",FontWeight.MEDIUM,20));
		Button moreInfo=new Button("More Info");
		moreInfo.setOnAction(e->c.plantInfo(e,p));
		
		//Add all to the flowpane
		fp.getChildren().addAll(j,plantNames,moreInfo);
		return fp;
	}
	/**
	 * Creates the flowpane that will allow the user to sort the available plants
	 * @return a flow pane consisting of a dropdown menu of available sort by
	 * options and a button to activate the sort
	 */
	public FlowPane createSidePane() {
		//Initialize the flowpane
		FlowPane sortPane = new FlowPane(Orientation.VERTICAL);
		
		//Create the button and dropdown menu for the flowpane and add them
		Button sortButton = new Button("Sort Plants");
		ObservableList<String> options = 
			    FXCollections.observableArrayList(
			        "Full Sun",
			        "Part Shade",
			        "Full Shade",
			        "Wet",
			        "Medium",
			        "Dry",
			        "Clay",
			        "Sandy",
			        "Loam",
			        "Herbacious",
			        "Woody"
			    );
		comboBox = new ComboBox<>(options);
		sortPane.getChildren().addAll(sortButton,comboBox);
		return sortPane;
	}
	
	public void updateList() {
		
	}
	/**
	 * A getter for searchScene
	 * @return	the searchScene attribute of the SearchView class
	 */
	public Scene getSearchScene() {
		return this.searchScene;
	}
}
