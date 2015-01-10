var testApp = angular.module('testApp', ['ui.router']);

testApp.config(function($stateProvider, $urlRouterProvider){
    
    $urlRouterProvider.otherwise('/');
    
    $stateProvider
    // route for the home page
            // HOME STATES AND NESTED VIEWS ========================================
        .state('home', {
            url: '/',
            templateUrl: 'home.html'
        })
        
        // ABOUT PAGE AND MULTIPLE NAMED VIEWS =================================
        .state('about', {
            url: '/about',
            templateUrl: '/static/daress_theme/js/partials/about.html'
        })
});

// create the controller and inject Angular's $scope

testApp.controller('mainController', function($scope) {
        // create a message to display in our view
        $scope.message = 'Everyone come and see how good I look!';
    });

    testApp.controller('aboutController', function($scope) {
        $scope.message = 'Look! I am an about page.';
    });

    testApp.controller('contactController', function($scope) {
        $scope.message = 'Contact us! JK. This is just a demo.';
    });