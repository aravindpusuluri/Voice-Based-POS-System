async function generateHome() {
	hideAll();
	document.getElementById("home").classList.add("activesec");
	document.getElementById("one").checked = true;
}
async function generateInvoice() {
	document.getElementById("test").innerHTML = "";
	hideAll();
	document.getElementById("displaycart").classList.add("activesec");
	var data = document.getElementById("data").value;
	eel.basket_printer()(dispInvoiceTable);
	eel.bill_amount()(dispInvoiceAmount);
}

async function generateAssistant() {
	hideAll();
	document.getElementById("assistant").classList.add("activesec");
	// for(i=0;i<voicedots.length;i++){
	// 	voicedots[i].classList.toggle("active");
	// }
	togglevoicedots();
	eel.tryblock();
	// var x = await
	// eel.myCommand()(dispTable);
	// for(i=0;i<voicedots.length;i++){
	// 	voicedots[i].classList.remove("active");
	// }
}
async function generateAssistant2() {
	hideAll();
	document.getElementById("assistant").classList.add("activesec");
	// for(i=0;i<voicedots.length;i++){
	// 	voicedots[i].classList.toggle("active");
	// }
	togglevoicedots();
	eel.feedBack();
	// var x = await
	// eel.myCommand()(dispTable);
	// for(i=0;i<voicedots.length;i++){
	// 	voicedots[i].classList.remove("active");
	// }
}
async function generateAssistant3() {
	hideAll();
	document.getElementById("assistant").classList.add("activesec");
	// for(i=0;i<voicedots.length;i++){
	// 	voicedots[i].classList.toggle("active");
	// }
	togglevoicedots();
	eel.billingIssues();
	// var x = await
	// eel.myCommand()(dispTable);
	// for(i=0;i<voicedots.length;i++){
	// 	voicedots[i].classList.remove("active");
	// }
}
async function generateproductReturns() {
	hideAll();
	document.getElementById("assistant").classList.add("activesec");
	// for(i=0;i<voicedots.length;i++){
	// 	voicedots[i].classList.toggle("active");
	// }
	togglevoicedots();
	eel.productReturns();
	// var x = await
	// eel.myCommand()(dispTable);
	// for(i=0;i<voicedots.length;i++){
	// 	voicedots[i].classList.remove("active");
	// }
}
async function generateBillingIssues() {
	hideAll();
	document.getElementById("assistant").classList.add("activesec");
	// for(i=0;i<voicedots.length;i++){
	// 	voicedots[i].classList.toggle("active");
	// }
	togglevoicedots();
	eel.billingIssues();
	// var x = await
	// eel.myCommand()(dispTable);
	// for(i=0;i<voicedots.length;i++){
	// 	voicedots[i].classList.remove("active");
	// }
}
async function generateServices() {
	hideAll();
	document.getElementById("services").classList.add("activesec");
}
// async function generateBill() {
// 	var data = document.getElementById("data").value;
// 	eel.basket_printer()(dispTable);
// }

async function generateInventory() {
	hideAll();
	document.getElementById("inventory").classList.add("activesec");
	var data = document.getElementById("data").value;
	eel.inv_printer()(dispStockTable);
}

async function generateMenu(){
	hideAll();
	document.getElementById("menu").classList.add("activesec");
}

function removeInitial(){
	sections=document.getElementsByTagName("section");
	for(i=0;i<sections.length;i++){
		sections[i].classList.remove("initial");
	}
}

function hideAll(){
	sections=document.getElementsByTagName("section");
	for(i=0;i<sections.length;i++){
		sections[i].style.display= "none";
		sections[i].classList.remove("activesec");
	}
	removevoicedots();
}
// function setImage(string) {
// 	alert(string)
// 	document.getElementById("test").innerHTML = string
// }
eel.expose(right_printer);
function right_printer(str) {
	  var chat = document.getElementById("chat");
	  var chathtml = "<div class='message-orange'><p class='message-content'>";
	  chathtml += str;
	  chathtml += "</p></div>";
	  chat.innerHTML += chathtml;
	  updateScroll();
}

eel.expose(left_printer);
function left_printer(str) {
	  var chat = document.getElementById("chat");
	  var chathtml = "<div class='message-blue'><p class='message-content'>";
	  chathtml += str;
	  chathtml += "</p></div>";
	  chat.innerHTML += chathtml;
	  updateScroll();
}

function updateScroll(){
    var element = document.getElementById("chat");
    element.scrollTop = element.scrollHeight;
}

eel.expose(togglevoicedots);
function togglevoicedots(){
	var voicedots = document.getElementsByClassName("voicedot");
	for(i=0;i<voicedots.length;i++){
		voicedots[i].classList.toggle("active");
	}
}

eel.expose(removevoicedots);
function removevoicedots(){
	var voicedots = document.getElementsByClassName("voicedot");
	for(i=0;i<voicedots.length;i++){
		voicedots[i].classList.remove("active");
	}
}

function dispInvoiceTable(table) {
	var tablehtml ="<h2 class='sqldisp'>Invoice Number: "+table[0][0]+"</h2><table class='sqldisp'><tr><th>Name</th><th></th><th>Cost</th><th></th><th>Quantity</th><th></th><th>Total</th><th></th>";
	var i,j=0;
	for(i=0;i<table.length;i++){
		if(i%2==0){
			tablehtml+="<tr style='background: lavender'>";
		}
		else{
			tablehtml+="<tr style='background: white'>"	;
		}
		for(j=1;j<table[i].length;j++){
			tablehtml += "<td><pre>"+table[i][j]+"\t</pre><td>";
		}
		tablehtml+="</tr>";
	}
	tablehtml+="</table>";
	document.getElementById("test").innerHTML = tablehtml;
	// var voicedots = document.getElementsByClassName("voicedot")
	// for(i=0;i<voicedots.length;i++){
	// 	voicedots[i].classList.remove("active");}
}
function dispInvoiceAmount(table) {
	tablehtml = document.getElementById("test").innerHTML;
	tablehtml+="<h2 class='sqldisp' style='text-align:right;'>Total Price: <span>&#8377<span>"+table[0][0]+"</h2>";
	document.getElementById("test").innerHTML = tablehtml;
}

function dispStockTable(table) {
	var tablehtml ="<table class='sqldisp'><tr><th>Product ID</th><th></th><th>Name</th><th></th><th>Cost</th><th></th><th>Stock Left</th><th></th>";
	var i,j=0;
	for(i=0;i<table.length;i++){
		if(i%2==0){
			tablehtml+="<tr style='background: lavender'>";
		}
		else{
			tablehtml+="<tr style='background: white'>"	;
		}
		for(j=0;j<table[i].length;j++){
			if(j==1 || j==4){
				continue;
			}
			tablehtml += "<td><pre>"+table[i][j]+"\t</pre><td>";
		}
		tablehtml+="</tr>";
	}
	tablehtml+="</table>";
	document.getElementById("stock").innerHTML = tablehtml;
	// var voicedots = document.getElementsByClassName("voicedot")
	// for(i=0;i<voicedots.length;i++){
	// 	voicedots[i].classList.remove("active");}
}

function initialDisp(){
	hideAll();
	removeInitial();
	document.getElementById("home").classList.add("activesec");
}
/////////////////////////test
function generateNewPage(){
	// eel.newPage();
	window.open("index.html","_self");
}
