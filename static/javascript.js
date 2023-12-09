function deleterecord(idno){
	var ok = confirm("Delete this record? => "+idno)
	if(ok){
		location.href="/deleterecord?idno="+idno
	}
}
function logout(){
	location.href="/logout"
}
function search(){
	location.href="/searchstudent"
}
function editrecord(idno,lastname,firstname,course,level,img){
	//document.forms['studentform']['flag'].value = id;
	document.forms['u_studentform']['u_idno'].value = idno;
	document.forms['u_studentform']['u_lastname'].value = lastname;
	document.forms['u_studentform']['u_firstname'].value = firstname;
	document.forms['u_studentform']['u_course'].value = course;
	document.forms['u_studentform']['u_level'].value = level;
	document.forms['u_studentform']['u_img'].value = img;
	document.getElementById('u_studentmodal').style.display='block'
}
function addrecord(){
	//document.forms['studentform']['flag'].value = '-'
	document.getElementById('studentmodal').style.display='block'
}

function generate_payroll(id,idno,lastname,firstname,position_desc,daily_rate){
	document.forms['studentform']['flag'].value = id;
	document.forms['studentform']['idno'].value = idno;
	document.forms['studentform']['name'].value = firstname + " " + lastname;
	document.forms['studentform']['rate'].value = daily_rate;
	document.forms['studentform']['d_r'].value = daily_rate;
	document.getElementById('MODAL').style.display='block'

}

function delete_payroll(id){
	var ok = confirm("Delete this payroll? => "+id)
	if(ok){
		location.href="/delete_payroll?id="+id
	}
}
function delete_emp(id){
	var ok = confirm("Delete this employee? => "+id)
	if(ok){
		location.href="/delete_emp?id="+id
	}
}
document.getElementById("days").addEventListener("change", function(){
		if (document.getElementById("days").value.length > 0){
			var number_of_days = parseInt(document.getElementById("days").value);
			
			if(number_of_days>=0){
				document.getElementById("salary").value = number_of_days*parseFloat(document.getElementById("rate").value)
			}else{
				document.getElementById("salary").value = "INVALID";
			}
		}

	});

var today = new Date();

var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
document.getElementById("date_to").valueAsDate = today;

function display_payroll(){
	location.href="/display_payroll"
}
function display_employee(){
	location.href="/studentlist/ok"
}
