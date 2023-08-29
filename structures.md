<class 'praw.models.reddit.submission.Submission'>
 A class for submissions to Reddit.


  Submission(id='164e4z5')

                 all_awardings = []
           allow_live_comments = False
               approved_at_utc = None
                   approved_by = None
                      archived = False
                        author = Redditor(name='Curious-College-3079')
 author_flair_background_color = None
        author_flair_css_class = None
         author_flair_richtext = []
      author_flair_template_id = None
             author_flair_text = None
       author_flair_text_color = None
             author_flair_type = 'text'
               author_fullname = 't2_8g68t62h'
             author_is_blocked = False
          author_patreon_flair = False
                author_premium = False
                      awarders = []
                 banned_at_utc = None
                     banned_by = None
                      can_gild = True
                  can_mod_post = False
                      category = None
                       clicked = False
                 comment_limit = 2048
                  comment_sort = 'confidence'
                      comments = <praw.models.comment_forest.CommentForest
                                 object at 0x7f7f3790eef0>
            content_categories = None
                  contest_mode = False
                       created = 1693303097.0
                   created_utc = 1693303097.0
               discussion_type = None
                 distinguished = None
                        domain = 'self.preguntaReddit'
                         downs = 0
                        edited = False
                         flair = <praw.models.reddit.submission.SubmissionFl…
                                 object at 0x7f7f3790dd80>
                      fullname = 't3_164e4z5'
                        gilded = 0
                      gildings = {}
                        hidden = False
                    hide_score = False
                            id = '164e4z5'
        is_created_from_ads_ui = False
              is_crosspostable = True
                       is_meta = False
           is_original_content = False
        is_reddit_media_domain = False
            is_robot_indexable = True
                       is_self = True
                      is_video = False
                         likes = None
   link_flair_background_color = ''
          link_flair_css_class = None
           link_flair_richtext = []
               link_flair_text = None
         link_flair_text_color = 'dark'
               link_flair_type = 'text'
                        locked = False
                         media = None
                   media_embed = {}
                    media_only = False
                           mod = <praw.models.reddit.submission.SubmissionMo…
                                 object at 0x7f7f3790e3e0>
                      mod_note = None
                 mod_reason_by = None
              mod_reason_title = None
                   mod_reports = []
                          name = 't3_164e4z5'
                     no_follow = True
                  num_comments = 6
                num_crossposts = 0
                num_duplicates = 0
                   num_reports = None
                       over_18 = True
       parent_whitelist_status = None
                     permalink = '/r/preguntaReddit/comments/164e4z5/es_un_f…
                        pinned = False
                          pwls = None
                    quarantine = False
                removal_reason = None
                    removed_by = None
           removed_by_category = None
                report_reasons = None
                         saved = False
                         score = 0
                  secure_media = None
            secure_media_embed = {}
                      selftext = 'Desde hace tiempo encontré el gusto a fumar
                                 (vape o cigarro) mientras veo p0rn0 y me
                                 toco. El efecto de la nicotina aumenta el
                                 placer al combinar ambas acciones al mismo
                                 tiempo. Nunca he escuchado de alguien que
                                 hiciera algo parecido. \n\n¿Alguien mas lo
                                 hace?\n\nQuisiera saber su opinión acerca de
                                 esto por favor. Gracias por su atención.'
                 selftext_html = '<!-- SC_OFF --><div class="md"><p>Desde
                                 hace tiempo encontré el gusto a fumar (vape
                                 o cigarro) mientras veo p0rn0 y me toco. El
                                 efecto de la nicotina aumenta el placer al
                                 combinar ambas acciones al mismo tiempo.
                                 Nunca he escuchado de alguien que hiciera
                                 algo parecido. </p>\n\n<p>¿Alguien mas lo
                                 hace?</p>\n\n<p>Quisiera saber su opinión
                                 acerca de esto por favor. Gracias por su
                                 atención.</p>\n</div><!-- SC_ON -->'
                  send_replies = True
                     shortlink = 'https://redd.it/164e4z5'
                       spoiler = False
                      stickied = False
                     STR_FIELD = 'id'
                     subreddit = Subreddit(display_name='preguntaReddit')
                  subreddit_id = 't5_38242'
       subreddit_name_prefixed = 'r/preguntaReddit'
         subreddit_subscribers = 57903
                subreddit_type = 'public'
                suggested_sort = None
                     thumbnail = 'self'
              thumbnail_height = None
               thumbnail_width = None
                         title = '¿Es un fetiche?'
              top_awarded_type = None
         total_awards_received = 0
                treatment_tags = []
                           ups = 0
                  upvote_ratio = 0.4
                           url = 'https://www.reddit.com/r/preguntaReddit/co…
                  user_reports = []
                    view_count = None
                       visited = False
              whitelist_status = None
                           wls = None
               add_fetch_param = def add_fetch_param(key, value): Add a
                                 parameter to be used for the next fetch.
                         award = def award(*, gild_type: str = 'gid_2',
                                 is_anonymous: bool = True, message: str =
                                 None) -> dict: Award the author of the item.
                    clear_vote = def clear_vote(): Clear the authenticated
                                 user's vote on the object.
                     crosspost = def crosspost(subreddit:
                                 'praw.models.Subreddit', *, flair_id:
                                 Optional[str] = None, flair_text:
                                 Optional[str] = None, nsfw: bool = False,
                                 send_replies: bool = True, spoiler: bool =
                                 False, title: Optional[str] = None) ->
                                 'praw.models.Submission': Crosspost the
                                 submission to a subreddit.
                        delete = def delete(): Delete the object.
         disable_inbox_replies = def disable_inbox_replies(): Disable inbox
                                 replies for the item.
                      downvote = def downvote(): Downvote the object.
                    duplicates = def duplicates(**generator_kwargs:
                                 Union[str, int, Dict[str, str]]) ->
                                 Iterator[ForwardRef('praw.models.Submission…
                                 Return a :class:`.ListingGenerator` for the
                                 submission's duplicates.
                          edit = def edit(body: str) ->
                                 Union[ForwardRef('praw.models.Comment'),
                                 ForwardRef('praw.models.Submission')]:
                                 Replace the body of the object with
                                 ``body``.
          enable_inbox_replies = def enable_inbox_replies(): Enable inbox
                                 replies for the item.
                          gild = def gild() -> dict: Alias for :meth:`.award`
                                 to maintain backwards compatibility.
                          hide = def hide(*, other_submissions:
                                 Optional[List[ForwardRef('praw.models.Submi…
                                 = None): Hide :class:`.Submission`.
                   id_from_url = def id_from_url(url: str) -> str: Return the
                                 ID contained within a submission URL.
                  mark_visited = def mark_visited(): Mark submission as
                                 visited.
                         parse = def parse(data: Dict[str, Any], reddit:
                                 'praw.Reddit') -> Any: Return an instance of
                                 ``cls`` from ``data``.
                         reply = def reply(body: str) ->
                                 Union[ForwardRef('praw.models.Comment'),
                                 ForwardRef('praw.models.Message'),
                                 NoneType]: Reply to the object.
                        report = def report(reason: str): Report this object
                                 to the moderators of its subreddit.
                          save = def save(*, category: Optional[str] = None):
                                 Save the object.
                        unhide = def unhide(*, other_submissions:
                                 Optional[List[ForwardRef('praw.models.Submi…
                                 = None): Unhide :class:`.Submission`.
                        unsave = def unsave(): Unsave the object.
                        upvote = def upvote(): Upvote the object.

Comments #########################################################################

 <class 'praw.models.reddit.comment.Comment'>
 A class that represents a Reddit comment.


  Comment(id='jya08nv')

                   all_awardings = []
                 approved_at_utc = None
                     approved_by = None
                        archived = False
                associated_award = None
                          author = Redditor(name='Spectrum-666')
   author_flair_background_color = None
          author_flair_css_class = None
           author_flair_richtext = []
        author_flair_template_id = None
               author_flair_text = None
         author_flair_text_color = None
               author_flair_type = 'text'
                 author_fullname = 't2_s5m0pnqa'
               author_is_blocked = False
            author_patreon_flair = False
                  author_premium = False
                        awarders = []
                   banned_at_utc = None
                       banned_by = None
                            body = 'No bro eso no es un fetiche al contrario
                                   te estas matando solo'
                       body_html = '<div class="md"><p>No bro eso no es un
                                   fetiche al contrario te estas matando
                                   solo</p>\n</div>'
                        can_gild = True
                    can_mod_post = False
                       collapsed = False
 collapsed_because_crowd_control = None
                collapsed_reason = None
           collapsed_reason_code = None
                    comment_type = None
                controversiality = 0
                         created = 1693339526.0
                     created_utc = 1693339526.0
                           depth = 0
                   distinguished = None
                           downs = 0
                          edited = False
                        fullname = 't1_jya08nv'
                          gilded = 0
                        gildings = {}
                              id = 'jya08nv'
                         is_root = True
                    is_submitter = False
                           likes = None
                         link_id = 't3_164e4z5'
                          locked = False
         MISSING_COMMENT_MESSAGE = 'This comment does not appear to be in the
                                   comment tree'
                             mod = <praw.models.reddit.comment.CommentModera…
                                   object at 0x7f7f3790d3c0>
                        mod_note = None
                   mod_reason_by = None
                mod_reason_title = None
                     mod_reports = []
                            name = 't1_jya08nv'
                       no_follow = True
                     num_reports = None
                       parent_id = 't3_164e4z5'
                       permalink = '/r/preguntaReddit/comments/164e4z5/es_un…
                  removal_reason = None
                         replies = <praw.models.comment_forest.CommentForest
                                   object at 0x7f7f3790fee0>
                  report_reasons = None
                           saved = False
                           score = 1
                    score_hidden = False
                    send_replies = True
                        stickied = False
                       STR_FIELD = 'id'
                      submission = Submission(id='164e4z5')
                       subreddit = Subreddit(display_name='preguntaReddit')
                    subreddit_id = 't5_38242'
         subreddit_name_prefixed = 'r/preguntaReddit'
                  subreddit_type = 'public'
                top_awarded_type = None
           total_awards_received = 0
                  treatment_tags = []
              unrepliable_reason = None
                             ups = 1
                    user_reports = []
╰──────────────────────────────────────────────────────────────────────────────╯
Redditors ########################################################################
<class 'praw.models.reddit.redditor.Redditor'>
 A class representing the users of Reddit.


  Redditor(name='Curious-College-3079')


        accept_chats = False
    accept_followers = True
          accept_pms = True
       awardee_karma = 0
       awarder_karma = 0
       comment_karma = 0
            comments = <praw.models.listing.mixins.redditor.SubListing object
                       at 0x7f7f37af9690>
             created = 1602515520.0
         created_utc = 1602515520.0
            fullname = 't2_8g68t62h'
      has_subscribed = True
  has_verified_email = True
    hide_from_robots = False
            icon_img = 'https://www.redditstatic.com/avatars/defaults/v2/ava…
                  id = '8g68t62h'
          is_blocked = False
         is_employee = False
           is_friend = False
             is_gold = False
              is_mod = False
          link_karma = 262
                name = 'Curious-College-3079'
               notes = <praw.models.mod_notes.RedditorModNotes object at
                       0x7f7f37af81c0>
 pref_show_snoovatar = False
       snoovatar_img = ''
      snoovatar_size = None
           STR_FIELD = 'name'
              stream = <praw.models.reddit.redditor.RedditorStream object at
                       0x7f7f37afa860>
         submissions = <praw.models.listing.mixins.redditor.SubListing object
                       at 0x7f7f37afa8c0>
           subreddit = UserSubreddit(display_name='u_Curious-College-3079')
         total_karma = 262
  VALID_TIME_FILTERS = {'hour', 'day', 'week', 'month', 'year', 'all'}
            verified = True
               block = def block(): Block the :class:`.Redditor`.
       controversial = def controversial(*, time_filter: str = 'all',
                       **generator_kwargs: Union[str, int, Dict[str, str]])
                       -> Iterator[Any]: Return a :class:`.ListingGenerator`
                       for controversial items.
            distrust = def distrust(): Remove the :class:`.Redditor` from
                       your whitelist of trusted users.
           downvoted = def downvoted(**generator_kwargs: Union[str, int,
                       Dict[str, str]]) ->
                       Iterator[Union[ForwardRef('praw.models.Comment'),
                       ForwardRef('praw.models.Submission')]]: Return a
                       :class:`.ListingGenerator` for items the user has
                       downvoted.
              friend = def friend(*, note: str = None): Friend the
                       :class:`.Redditor`.
         friend_info = def friend_info() -> 'praw.models.Redditor': Return a
                       :class:`.Redditor` instance with specific
                       friend-related attributes.
           from_data = def from_data(reddit, data): Return an instance of
                       :class:`.Redditor`, or ``None`` from ``data``.
                gild = def gild(*, months: int = 1): Gild the
                       :class:`.Redditor`.
              gilded = def gilded(**generator_kwargs: Union[str, int,
                       Dict[str, str]]) -> Iterator[Any]: Return a
                       :class:`.ListingGenerator` for gilded items.
            gildings = def gildings(**generator_kwargs: Union[str, int,
                       Dict[str, str]]) ->
                       Iterator[Union[ForwardRef('praw.models.Comment'),
                       ForwardRef('praw.models.Submission')]]: Return a
                       :class:`.ListingGenerator` for items the user has
                       gilded.
              hidden = def hidden(**generator_kwargs: Union[str, int,
                       Dict[str, str]]) ->
                       Iterator[Union[ForwardRef('praw.models.Comment'),
                       ForwardRef('praw.models.Submission')]]: Return a
                       :class:`.ListingGenerator` for items the user has
                       hidden.
                 hot = def hot(**generator_kwargs: Union[str, int, Dict[str,
                       str]]) -> Iterator[Any]: Return a
                       :class:`.ListingGenerator` for hot items.
             message = def message(*, from_subreddit:
                       Union[ForwardRef('praw.models.Subreddit'), str,
                       NoneType] = None, message: str, subject: str): Send a
                       message to a :class:`.Redditor` or a
                       :class:`.Subreddit`'s moderators (modmail).
           moderated = def moderated() ->
                       List[ForwardRef('praw.models.Subreddit')]: Return a
                       list of the redditor's moderated subreddits.
        multireddits = def multireddits() ->
                       List[ForwardRef('praw.models.Multireddit')]: Return a
                       list of the redditor's public multireddits.
                 new = def new(**generator_kwargs: Union[str, int, Dict[str,
                       str]]) -> Iterator[Any]: Return a
                       :class:`.ListingGenerator` for new items.
               parse = def parse(data: Dict[str, Any], reddit: 'praw.Reddit')
                       -> Any: Return an instance of ``cls`` from ``data``.
               saved = def saved(**generator_kwargs: Union[str, int,
                       Dict[str, str]]) ->
                       Iterator[Union[ForwardRef('praw.models.Comment'),
                       ForwardRef('praw.models.Submission')]]: Return a
                       :class:`.ListingGenerator` for items the user has
                       saved.
                 top = def top(*, time_filter: str = 'all',
                       **generator_kwargs: Union[str, int, Dict[str, str]])
                       -> Iterator[Any]: Return a :class:`.ListingGenerator`
                       for top items.
            trophies = def trophies() ->
                       List[ForwardRef('praw.models.Trophy')]: Return a list
                       of the redditor's trophies.
               trust = def trust(): Add the :class:`.Redditor` to your
                       whitelist of trusted users.
             unblock = def unblock(): Unblock the :class:`.Redditor`.
            unfriend = def unfriend(): Unfriend the :class:`.Redditor`.
             upvoted = def upvoted(**generator_kwargs: Union[str, int,
                       Dict[str, str]]) ->
                       Iterator[Union[ForwardRef('praw.models.Comment'),
                       ForwardRef('praw.models.Submission')]]: Return a
                       :class:`.ListingGenerator` for items the user has
                       upvoted.


