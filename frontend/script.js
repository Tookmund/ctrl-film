const app = new Vue({
	el: "#app",
	data: {
		isFormState: true, // false = search results page
		url: "",
		text: [],
		query: "",
		statusMessage: ""
	},
	methods: {
		submitURL: function () {
			var app = this;
			fetch("http://search-in-video.tookmund.com/video", {  
				method: 'POST',
				body: "url=" + app.url
			})
			.then( function (data) {
				this.statusMessage = "Loading...";
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
			})  
			.catch( function (error) {  
				this.errorMessage = "Error :( please try again."
			});
		},
		
		goBack: function () {
			this.isFormState = true;
			this.query = "";
			this.errorMessage = "";
		}
	}
});