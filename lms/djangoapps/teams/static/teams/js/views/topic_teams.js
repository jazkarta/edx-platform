;(function (define) {
    'use strict';

    define(['backbone', 'gettext', 'teams/js/views/teams',
            'text!teams/templates/team-actions.underscore'],
        function (Backbone, gettext, TeamsView, teamActionsTemplate) {
            var TopicTeamsView = TeamsView.extend({
                events: {
                    'click a.browse-teams': 'browseTeams',
                    'click a.search-teams': 'searchTeams',
                    'click a.create-team': 'showCreateTeamForm'
                },

                initialize: function(options) {
                    TeamsView.prototype.initialize.call(this, options);
                    _.bindAll(this, 'browseTeams', 'searchTeams', 'showCreateTeamForm');
                },

                render: function() {
                    TeamsView.prototype.render.call(this);

                    if (this.teamMemberships.canUserCreateTeam()) {
                        var message = interpolate_text(
                            _.escape(gettext("Try {browse_span_start}browsing all teams{span_end} or {search_span_start}searching team descriptions{span_end}. If you still can't find a team to join, {create_span_start}create a new team in this topic{span_end}.")),
                            {
                                'browse_span_start': '<a class="browse-teams" href="">',
                                'search_span_start': '<a class="search-teams" href="">',
                                'create_span_start': '<a class="create-team" href="">',
                                'span_end': '</a>'
                            }
                        );
                        this.$el.append(_.template(teamActionsTemplate, {message: message}));
                    }
                    return this;
                },

                browseTeams: function (event) {
                    event.preventDefault();
                    Backbone.history.navigate('browse', {trigger: true});
                },

                searchTeams: function (event) {
                    event.preventDefault();
                    // TODO! Will navigate to correct place once required functionality is available
                    Backbone.history.navigate('browse', {trigger: true});
                },

                showCreateTeamForm: function (event) {
                    event.preventDefault();
                    Backbone.history.navigate('topics/' + this.teamParams.topicID + '/create-team', {trigger: true});
                }
            });

            return TopicTeamsView;
        });
}).call(this, define || RequireJS.define);
