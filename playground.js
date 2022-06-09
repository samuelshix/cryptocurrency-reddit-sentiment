'use strict';
const snoowrap = require('snoowrap');

const r = new snoowrap({
    userAgent: 'web:crypto-comment-sentiment:v1.0.0 (by /u/kash_sam_)',
    clientId: '3B_hPuLSNInJTsozWMHqcA',
    clientSecret: 'mMcsjS3apcp-wIxm2mcGNlEaAZsn_A',
    refreshToken: '1465172366980-e2dmH8dhM9fuRe9eQSWOHVGhaSuOSQ'
})

// r.getSubreddit('cryptocurrency').getTop({time:'week',limit: 3}).then(data=>console.log);
// r.getSubmission('4j8p6d').expandReplies({limit: 1, depth: 2}).then(console.log);
// .expandReplies({limit: Infinity, depth: Infinity}).then(console.log)
// refresh token: 1465172366980-e2dmH8dhM9fuRe9eQSWOHVGhaSuOSQ
// access token: 1465172366980-RfQN5vIG_AJF9IkIwCvaXMtmxJsjfg
