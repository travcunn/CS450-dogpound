$matched = $("<p class='valid'>Passwords Match</p>")
$unmatched = $("<p class='invalid'>Passwords Don't Match</p>")

$(document).ready(function(){
	// set page name to a variable
	var pageName = location.pathname.split('/').slice(-1)[0];
	
// 	if (pageName == 'registration.html') || (pageName == 'resetPassword') {
		if ($('#password').val() != null) {
			// event if first Password field is changed
			$('#password').keyup(function(){
				if ($('#password').val() == $('#password_match').val()){
					$('#pw_match').html($matched);
					$('#regSubmit').show();
				}
				else {
					$('#pw_match').html($unmatched);
					$('#regSubmit').hide();
				};
			});

			// event if Retype Password field is changed
			$('#password_match').keyup(function(){
				if ($('#password').val() == $('#password_match').val()){
					$('#pw_match').html($matched);
					$('#regSubmit').show();
				}
				else {
					$('#pw_match').html($unmatched);
					$('#regSubmit').hide();
				};
			});
		}
// 	} // end if statement to check page name
});
