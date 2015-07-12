#!/bin/bash
tshark -r $1 -T fields \
-e frame.time \
-e frame.len \
-e frame.protocols \
-e ip.src \
-e ip.dst \
-e ip.proto \
-e tcp.srcport \
-e tcp.dstport \
-e tcp.seq \
-e tcp.ack \
-e tcp.flags \
-e tcp.flags.syn \
-e tcp.flags.ack \
-e tcp.window_size \
-e udp.srcport \
-e udp.dstport \
-e http.accept \
-e http.accept_encoding \
-e http.accept_language \
-e http.cache_control \
-e http.connection \
-e http.content_type \
-e http.cookie \
-e http.host \
-e http.referer \
-e http.request \
-e http.request.full_uri \
-e http.request.method \
-e http.request.uri \
-e http.request.version \
-e http.response \
-e http.response.code \
-e http.response.phrase \
-e http.server \
-e http.set_cookie \
-e http.user_agent \
-e http.content_length \
-e http.content_length_header \
-e http.www_authenticate \
-e dns.count.add_rr \
-e dns.count.answers \
-e dns.count.auth_rr \
-e dns.count.queries \
-e dns.flags \
-e dns.id \
-e dns.qry.class \
-e dns.qry.name \
-e dns.dry.type \
-e dns.resp.addr \
-e dns.resp.class \
-e dns.resp.len \
-e dns.resp.name \
-e dns.resp.ns \
-e dns.resp.primaryname \
-e dns.resp.ttl \
-e dns.resp.type \
-e dns.response_to \
-e dns.time \
-e ssl.record.content_type \
-e ssl.record.version \
-e ssl.record.length \
-e ssl.handshake.type \
-e ssl.alert_message.desc \
-e frame.time_epoch \
-e eth.src \
-e eth.dst \
> $2