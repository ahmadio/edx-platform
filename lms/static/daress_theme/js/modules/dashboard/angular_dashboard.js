var dashboard = angular.module('dashboard', ['ui.router']);

dashboard.config(['$stateProvider', '$urlRouterProvider', '$urlMatcherFactoryProvider', function($stateProvider, $urlRouterProvider){
    
    $urlRouterProvider.otherwise('/');
    
    $stateProvider
    // route for the home page
            // HOME STATES AND NESTED VIEWS ========================================
        .state('home', {
            url: '/',
            templateUrl: 'timeline.tmpl.html'
        })
        
        // ABOUT PAGE AND MULTIPLE NAMED VIEWS =================================
        .state('timeline', {
            url: '/timeline',
            templateUrl: 'timeline.tmpl.html'
        })
    
        .state('notifications', {
            url: '/notifications',
            templateUrl: 'notifications.tmpl.html'
        })
    
        .state('my-courses', {
            url: '/my-courses',
            templateUrl: 'my-courses.tmpl.html'
        })
    
        .state('pinding-enrolls', {
            url: '/pinding-enrolls',
            templateUrl: 'pinding-enrolls.tmpl.html'
        })
    
        .state('payments', {
            url: '/payments',
            templateUrl: 'payments.tmpl.html'
        });
}]);

// create the controller and inject Angular's $scope

dashboard.controller('mainController', function($scope) {
        // create a message to display in our view
        $scope.message = 'Everyone come and see how good I look!';
    });

    dashboard.controller('aboutController', function($scope) {
        $scope.message = 'Look! I am an about page.';
    });

    dashboard.controller('contactController', function($scope) {
        $scope.message = 'Contact us! JK. This is just a demo.';
    });