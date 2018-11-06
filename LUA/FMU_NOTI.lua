#!/usr/bin/env lua

M = {}

trace.enable()
function M.outbound_NOTIFY(msg)
    msg:removeContentBody("application/simple-message-summary")
    msg:addContentBody("application/simple-message-summary", "Messages-Waiting: no")
end

return M
