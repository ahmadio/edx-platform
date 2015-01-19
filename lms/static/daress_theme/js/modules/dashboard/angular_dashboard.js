var dashboard = angular.module('dashboard', ['ui.router']);

dashboard.config(['$stateProvider', '$urlRouterProvider', '$urlMatcherFactoryProvider', function($stateProvider, $urlRouterProvider){
    
    $urlRouterProvider.otherwise('/');
    
    $stateProvider
    // route for the home page
            // HOME STATES AND NESTED VIEWS ========================================
        .state('home', {
            url: '/',
            templateUrl: 'my-courses.tmpl.html'
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
            templateUrl: 'payments.tmpl.html',
            controller: 'payments'
        });
}]);

// create the controller and inject Angular's $scope

dashboard.controller('payments', function($scope) {
    $scope.isChargeFormShown = false;
    $scope.showChargForm = function () {
        $scope.isChargeFormShown = !$scope.isChargeFormShown;
    };

    $scope.submitForm = function (chargeId) {
        $('#'+chargeId+' form').submit();
    };
});