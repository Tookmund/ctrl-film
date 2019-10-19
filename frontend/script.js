const app = new Vue({
	el: "#app",
	data: {
		isFormState: true, // false = search results page
		url: "",
		text: [],
		query: "",
		statusMessage: "",
		token: "",
		isSearching: false
	},
	methods: {
		submitURL: function () {
			var app = this;
			this.statusMessage = "Loading...";
			this.isSearching = true;
			fetch("http://search-in-video.tookmund.com/video", {  
				method: 'POST',
				headers: {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': '*/*'},
				body: encodeURI("url=" + app.url)
			})
			.then( function (response) {
				response.json().then( function (json) {
					app.token = json["token"]
				});
			})  
			.catch( function (error) {
				this.statusMessage = "Error :( please try again."
			});
		},
		submitFile: function() {
			this.statusMessage = "Loading...";
			this.isSearching = true;
			fetch("http://search-in-video.tookmund.com/video", {  
				method: 'POST',
				body: document.querySelection('input[type=file]').files[0]
			})
			.then( function (response) {
				response.json().then( function (json) {
					app.token = json["token"]
				});
			})
			.catch( function (error) {
				this.statusMessage = "Error :( please try again."
			});
		},
		
		goBack: function () {
			this.isFormState = true;
			this.query = "";
			this.statusMessage = "";
			this.token = "";
			this.isSearching = false;
		},
		
		cancel: function () {
			this.statusMessage = "";
			this.token = "";
			this.isSearching = false;
		},
		
		checkToken: function () {
			var app = this;
			if (this.token == "") {
				return;
			}
			fetch("http://search-in-video.tookmund.com/video/?token="+encodeURI(app.token))
			.then( function (response) {
				if (response.status != 200) {
					return;
				}
				console.log(response);
				response.json().then( function (json) {
					while (app.text.length > 0) {
						app.text.pop();
					}
					screen = json['screen']
					for (var timestamp in screen) {
						app.text.push({
							timestamp: timestamp,
							text: screen[timestamp]
						});
					}
					app.text.push({
						timestamp: "Audio Transcript",
						text: json['audio']
					});
					app.isFormState = false;
				});
			});
		}
	},
	computed: {
		isReadOnly: function () {
			if (this.isSearching) {
				return true;
			}
			return false;
		}
	},
	mounted: function () {
		window.setInterval(() => {
			this.checkToken()
		}, 5000)
	}
});
