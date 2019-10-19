const app = new Vue({
	el: "#app",
	data: {
		isFormState: true, // false = search results page
		url: "",
		text: [],
		query: "",
		statusMessage: "",
		token: ""
	},
	methods: {
		submitURL: function () {
			var app = this;
			this.statusMessage = "Loading...";
			fetch("http://search-in-video.tookmund.com/video", {  
				method: 'POST',
				headers: {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': '*/*'},
				body: encodeURI("url=" + app.url)
			})
			.then( function (response) {
				response.json().then( function (json) {
					console.log(json);
				});
			})  
			.catch( function (error) {
				this.statusMessage = "Error :( please try again."
			});
		},
		
		goBack: function () {
			this.isFormState = true;
			this.query = "";
			this.errorMessage = "";
			this.token = "";
		}
	}
});

/*

console.log(data);
				data.json().then( function (json) {
					while (app.text.length > 0) {
						app.text.pop();
					}
					for (var timestamp in json) {
						app.text.push({
							timestamp: timestamp,
							text: json[timestamp]
						});
					}
					app.isFormState = false;
				});
				
*/