Vue.component('singIn-form', { 
	data: function(){
		return{
			cars:[
				{model: "BMW"},
				{model: "Volvo"}
			]
		}
	},
	template: '<div><div class="car" v-for="car in car"><p>{{ car.model }}</p></div></div>'
})


var app = new Vue({
  el: '#sing',
  data: {
    message: 'Hello Vue!'
  }
})
